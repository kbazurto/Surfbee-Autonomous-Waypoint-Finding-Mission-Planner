import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
from random import randint
import math

import matlab.engine


import mapsexample as gmap
import kalman as kal


##########


import socket
import sys

import json


# worker.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time




import numpy as np

###

# Distance from RSSI

###








class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    sign = pyqtSignal(object)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        '''
        for i in range(1, 100):
            time.sleep(1)
            #self.intReady.emit(i)
            sys.stdout.write("HI")

        #self.finished.emit()
        '''

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(self.sock)

        # Connect the socket to the port where the server is listening
        host = socket.gethostname()
        print(host)
        #server_address = ('192.168.43.195', 49152) #195 gabe, 89 lach
        #server_address = ('127.0.0.1', 8080)
        server_address = ('192.168.43.195', 49152)
        print('connecting to %s port %s' % server_address)
        self.sock.connect(server_address)

        try:
            '''
            # Send data
            message = 'This is the message.  It will be repeated.'
            print >>sys.stderr, 'sending "%s"' % message
            sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            '''

            #self.sock.send(b"hello!")

            while True:
                data = self.sock.recv(1000)
                #amount_received += len(data)
                #print("er")
                if data != '':

                    print('received "%s"' % data)
                    #self.sock.sendall(b"ACK\n\r")
                    self.sign.emit(data)

                #self.sleep(2)

        finally:
            print('closing socket')
            self.sock.close()



############



class App(QMainWindow):

    def __init__(self):
        super().__init__()


        self.label = QLabel("0")
        


        
        # 1 - create Worker and Thread inside the Form
        self.obj = Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.obj.sign.connect(self.signal_get)

        # 3 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.obj.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj.procCounter)

        # * - Thread finished signal will close the app if you want!
        #self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        self.thread.start()
        
        
        self.startfilt = 0
        self.kalman = 0

        self.orient = 0
        self.latlng = [0,0]
        self.waypt = [-27.500046, 153.0161085]

        self.theta = 0
        self.veloc = [0,0]
        self.t = 1

        
        

        self.tree = TreeList(self)
        self.wayptlab = QLabel()
        self.curposlab = QLabel()
        self.golab = QLabel()
        self.markers = {}
        
        self.auto = 0

        self.left = 10
        self.top = 10
        self.title = 'RSSI Multilateration Localisation'
        self.width = 1000
        self.height = 1000
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        #self.plotcanv = PlotCanvas(self, width=5, height=4)

        #self.plotcanv.move(0,0)


        grid = QtWidgets.QGridLayout(self.centralWidget())



        API_KEY = "AIzaSyCSDgvApmlrnRK2FCab-r_5k6RWgBHBjZs"

        self.w = gmap.QGoogleMap(api_key=API_KEY)
        grid.addWidget(self.w, 0, 0, 3, 3)

        #w.resize(640, 480)
        #self.w.resize(500,500)
        self.w.show()
        self.w.waitUntilReady()
        self.w.setZoom(18)

        lat, lng = self.w.centerAtAddress("UQ Lakes")
        if lat is None and lng is None:
            lat, lng = -27.500046, 153.0161085
            self.w.centerAt(lat, lng)




        
        self.markers['waypt'] = [-27.500046, 153.0161085]
        self.markers['curpos'] = [-27.500546, 153.015245]
        self.latlng = [-27.500546, 153.015245]


        self.w.addMarker("waypt", lat, lng, **dict(
            icon="http://maps.google.com/mapfiles/ms/icons/red.png",
            draggable=True,
            title="Waypoint!"
        ))

        self.w.markerMoved.connect(self.marker_move)


        self.w.addMarker("curpos", -27.500546, 153.015245, **dict(
            icon="http://maps.google.com/mapfiles/ms/icons/sailing.png",
            draggable=True,
            title="Current Position!"
        ))



        '''
        self.messages = MessageList(self)
        self.messages.move(500,0)
        self.messages.resize(300,400)
        '''

        
        #self.tree.move(500,0)
        grid.addWidget(self.tree, 0, 3, 3, 3)
        self.tree.resize(500, 800)
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["Timestamp", "GPS", "Accel", "Gyro", "Mag"])

        #j = json.loads('{"rssi":"-40", "rssi2":"-40", "rssi3":"-40", "rssi4":"-40", "ultra":{"main":"-40"}, "ultra2":{"main":"-40"}, "ultra3":{"main":"-40"}, "ultra4":{"main":"-40"}, "acc": {"x": "0", "y":"0", "z":"0"}, "gyro": {"x": "0", "y":"0", "z":"0"}}')

        #self.tree._populate(j)


        

        self.wayptlab.setText("Waypoint: Lat %f      Lng %f" % (self.markers['waypt'][0],self.markers['waypt'][1]))
        text = "Current Position: Lat %f      Lng %f      Orient %d degrees" % (self.markers['curpos'][0],self.markers['curpos'][1], self.orient)
        self.curposlab.setText(text)
        self.golab.setText("Waiting")
        #self.curposlab.setText("Current Position: Lat %f      Lng %f      Orient %d" % (self.markers['curpos'][0],self.markers['curpos'][1], self.orient))

        grid.addWidget(self.wayptlab, 3, 0, 1, 2)
        grid.addWidget(self.curposlab, 4, 0, 1, 2)
        grid.addWidget(self.golab, 4, 2, 1, 1)



        self.ubutton = QPushButton('Forward', self)
        self.ubutton.setToolTip('This s an example button')
        grid.addWidget(self.ubutton, 3, 4, 1, 1)

        self.ubutton.clicked.connect(self.butt_forward)

        self.dbutton = QPushButton('Stop', self)
        self.dbutton.setToolTip('This s an example button')
        grid.addWidget(self.dbutton, 4, 4, 1, 1)

        self.dbutton.clicked.connect(self.butt_stop)
        #button.resize(140,100)

        self.lbutton = QPushButton('Left', self)
        self.lbutton.setToolTip('This s an example button')
        grid.addWidget(self.lbutton, 4, 3, 1, 1)

        self.lbutton.clicked.connect(self.butt_left)


        self.rbutton = QPushButton('Right', self)
        self.rbutton.setToolTip('This s an example button')
        grid.addWidget(self.rbutton, 4, 5, 1, 1)

        self.rbutton.clicked.connect(self.butt_right)


        self.autobutton = QPushButton('Start Autopilot', self)
        self.autobutton.setToolTip('This s an example button')
        grid.addWidget(self.autobutton, 3, 2, 1, 1)

        self.autobutton.clicked.connect(self.butt_auto)

        '''
        self.labelTime = QLabel()
        self.update_labelTime()
        self.setCentralWidget(self.labelTime)#
        '''

        self.timer = QTimer()
        #self.timer.timeout.connect(self.update_labelTime)
        #self.timer.timeout.connect(self.moveMarkerTest)
        self.timer.start(1000) # repeat self.update_labelTime every 1 sec







        self.show()

        #using_q_thread()

    def update_labelTime(self):

        time_str = "Current time: {0}".format(QTime.currentTime().toString())
        self.labelTime.setText(time_str)


    def moveMarkerTest(self):

        lat = -27.49836900
        lng = 153.01439000

        lat = lat + 0.00001*randint(0, 9)
        lng = lng + 0.00001*randint(0, 9)

        self.w.moveMarker("curpos", lat, lng)





    def signal_get(self, sign):
        #print("GOTEEM %s" % sign)

        j = json.loads('{"rssi0": -12, "rssi1": -12, "rssi2": -12, "rssi3": -12}')

        try:
            dataload = json.loads(sign)

            self.tree._populate(dataload)
            self.sensor_fuse(dataload)






        except ValueError:
            print("LOL")

        #print(b["acc"])

    def butt_auto(self):

        self.auto = 1



    def butt_forward(self):

        sock = self.obj.sock

        print("Forward")
        #sock.send(b"F\n")

        self.auto = 0


    def butt_stop(self):

        sock = self.obj.sock

        print("Stop")
        #sock.send(b"S\n")

        self.auto = 0

    def butt_left(self):

        sock = self.obj.sock

        print("Left")
        #sock.send(b"L\n")

        self.auto = 0

    def butt_right(self):

        sock = self.obj.sock

        print("Right")
        #sock.send(b"R\n")

        self.auto = 0

        #self.messages._populate(sign)

    def marker_move(self, key, lat, lng):

        self.markers[key] = [lat,lng]
        
        print("marker %s moved to %f %f" % (key, lat, lng))

        if key == 'waypt' :
            self.wayptlab.setText("Waypoint: Lat %f      Lng %f" % (self.markers['waypt'][0],self.markers['waypt'][1]))
            self.waypt = [lat,lng]

        if key == 'curpos' :
            text = "Current Position: Lat %f      Lng %f      Orient %d degrees" % (self.markers['curpos'][0],self.markers['curpos'][1], self.orient)
            self.curposlab.setText(text)
            self.latlng = [lat,lng]



    def sensor_fuse(self, data):

        gps = data["gps"]
        accel = data["acc"]
        gyro = data["gyro"]
        mag = data["mag"]



        #Get Orientation from Magnetometer
        mx = int(mag['x'])
        my = int(mag['y']) - 100

        if mx != 0:

            self.theta = math.atan2(my,mx)*180/math.pi

            if self.theta < 0:
                self.orient = 360 + self.theta

            else:
                self.orient = self.theta

        print(self.orient)

        #text = "Current Position: Lat %f      Lng %f      Orient %d degrees" % (self.markers['curpos'][0],self.markers['curpos'][1], self.orient)
        #self.curposlab.setText(text)


        #calc velocity
        ax = float(accel["x"]) / 100
        ay = float(accel["y"]) / 100
        self.veloc = [self.veloc[0] + ax*self.t, self.veloc[1] + ay*self.t]

        s = [self.veloc[0]*self.t + (ax/2 * (self.t**2)), self.veloc[1]*self.t + (ay/2 * (self.t**2))]

        print(s)


        #GPS Data
        latitude = float(gps["lat"])
        longitude = float(gps["long"])

        if latitude != 0 and longitude != 0:

            

            if self.startfilt == 0:

                ndim = 4
                xcoord = longitude
                ycoord = latitude
                vx = 0 #m.s
                vy = 0 #m/s
                dt = 1 #sec
                meas_error = 5 #m


                #init filter
                proc_error = 0.5;
                init_error = 0.5;
                x_init = np.array( [xcoord, ycoord, vx, vy] ) #introduced initial xcoord error of 10m
                cov_init=init_error*np.eye(ndim)

                self.kalman = kal.Kalman(x_init, cov_init, meas_error/10, proc_error)


                print("INITKALMAN\n\n\n")




            self.startfilt = 1

            self.w.moveMarker("curpos", latitude, longitude)
            self.w.centerAt(latitude, longitude)


        else:

            print("accel based localise")
            #no new gps so calc via accel + orient
            s = np.array([[s[0]], [s[1]]])
            print(s)

            thetarad = (360 - self.orient) * math.pi / 180

            rotmat = np.array([[math.cos(thetarad), -math.sin(thetarad)], [math.sin(thetarad), math.cos(thetarad)]])
            print(rotmat)

            rots = np.matmul(rotmat, s)
            print(rots)

            rots[0] = rots[0] * 0.000010526
            rots[1] = rots[1] * 0.00000898

            latitude = self.latlng[0] + rots[1] # y is lat
            longitude = self.latlng[1] + rots[0] #x is long



        if self.kalman != 0:

            self.kalman.update([longitude, latitude])
            lnglat = self.kalman.x_hat

            longitude = lnglat[0]
            latitude = lnglat[1]

            print(longitude, latitude)


            self.w.moveMarker("curpos", latitude, longitude)
            self.w.centerAt(latitude, longitude)
            self.marker_move("curpos", latitude, longitude)



        

            wx = self.waypt[1] / 0.0000105
            wy = self.waypt[0] / 0.000009

            cx = self.latlng[1] / 0.0000105
            cy = self.latlng[0] / 0.000009

            vect = [wx - cx, wy - cy]



            auto = math.atan2(vect[0], vect[1]) * 180 / math.pi

            if auto < 0:
                auto = 360 + auto

            print("autopilot theta: %d" % auto)

            cmd = "stop"

            if auto > self.orient:

                if auto - self.orient < 180 and auto - self.orient > 20:
                    cmd = "right"

                elif auto - self.orient > 180 and auto - self.orient < 340:
                    cmd = "left"

                else:
                    cmd = "straight"

            elif self.orient > auto:
                if abs(auto - self.orient) < 180 and abs(auto - self.orient) > 20:
                    cmd = "left"

                elif abs(auto - self.orient) > 180 and abs(auto - self.orient) < 340:
                    cmd = "right"

                else:
                    cmd = "straight"

            


            v = np.array(vect)

            dist = np.linalg.norm(v)

            if dist < 2:
                cmd = "stop"

            self.golab.setText(cmd)




class TreeList(QTreeWidget):

    def __init__(self, parent=None):
        super(QTreeWidget,self).__init__(parent)
        self.items = []
        self.setParent(parent)

        '''
        tw.addTopLevelItem(lsss[0])
        tw.addTopLevelItem(l2)
        '''


    def _populate(self, j):
        ''' Fill the list with images from the
            current directory in self._dirpath. '''

        # In case we're repopulating, clear the list
        #self.clear()

        tstamp = "{0}".format(QTime.currentTime().toString())
        gpsstr = "lat %s\nlong %s" % (j["gps"]["lat"], j["gps"]["long"])
        accstr = "x %s\ny %s\nz %s" % (j["acc"]["x"], j["acc"]["y"], j["acc"]["z"])
        gyrostr = "x %s\ny %s\nz %s" % (j["gyro"]["x"], j["gyro"]["y"], j["gyro"]["z"])
        magstr = "x %s\ny %s\nz %s" % (j["mag"]["x"], j["mag"]["y"], j["mag"]["z"])



        newItem = QTreeWidgetItem([tstamp, gpsstr, accstr, gyrostr, magstr])

        self.items = [newItem] + self.items

        for i in range(len(self.items)):
            self.takeTopLevelItem(i)

        if len(self.items) > 4:
            del self.items[-1]

        #items = [itemscop[i+1] for i in range(1, len(itemscop) )]

        # Create a list item for each image file,
        # setting the text and icon appropriately


        '''
        for i in self.items:
            self.addTopLevelItem(i)
        '''

        self.addTopLevelItem(newItem)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
