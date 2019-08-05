
import pylab
import numpy



ndim = 4
xcoord = 2.0
ycoord = 2.0
vx = 0.2 #m.s
vy = 0.2 #m/s
dt = 1 #sec
meas_error = 0.5 #m


#init filter
proc_error = 0.2;
init_error = 0.3;
x_init = numpy.array( [xcoord, ycoord, vx, vy] ) #introduced initial xcoord error of 10m
cov_init=init_error*numpy.eye(ndim)




class Kalman:
    def __init__(self, x_init, cov_init, meas_err, proc_err):
        self.ndim = len(x_init)
        self.A = numpy.array([(1, 0, dt, 0), (0, 1, 0, dt), (0, 0, 1, 0), (0, 0, 0, 1)]);
        self.H = numpy.array([(1, 0, 0, 0), (0, 1, 0, 0)])
        self.x_hat =  x_init
        self.cov = cov_init
        self.Q_k = numpy.eye(ndim)*proc_err
        self.R = numpy.eye(len(self.H))*meas_err

    def update(self, obs):

        # Make prediction
        self.x_hat_est = numpy.dot(self.A,self.x_hat)
        self.cov_est = numpy.dot(self.A,numpy.dot(self.cov,numpy.transpose(self.A))) + self.Q_k

        # Update estimate
        self.error_x = obs - numpy.dot(self.H,self.x_hat_est)
        self.error_cov = numpy.dot(self.H,numpy.dot(self.cov_est,numpy.transpose(self.H))) + self.R
        self.K = numpy.dot(numpy.dot(self.cov_est,numpy.transpose(self.H)),numpy.linalg.inv(self.error_cov))
        self.x_hat = self.x_hat_est + numpy.dot(self.K,self.error_x)
        if ndim>1:
            self.cov = numpy.dot((numpy.eye(self.ndim) - numpy.dot(self.K,self.H)),self.cov_est)
        else:
            self.cov = (1-self.K)*self.cov_est
