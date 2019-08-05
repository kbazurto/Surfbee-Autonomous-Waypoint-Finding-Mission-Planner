
#include "WaspGPS.h"

//#include <WaspGPS.h>


#define TIMEOUT 240
#define WAIT 1000
bool status;

char send_buffer[100], buffer2[100], buffer3[100];

float lat;
float longi;
unsigned long now;

void setup()
{
  USB.ON();
  // put your setup code here, to run once:\
  
  pinMode(DIGITAL5, OUTPUT);
  //pinMode(DIGITAL7, INPUT);
  digitalWrite(DIGITAL5, LOW);
  
 // int p = digitalRead(DIGITAL7);
  //USB.print(p);
  
  //USB.println(F("GPS"));
  GPS.ON();
  
}



void loop()
{
 
   USB.println("\nHERE");
/*
 serialFlush(1);
  GPS.begin();
  status = GPS.waitForSignal(TIMEOUT);
  if( status == true){
    //USB.println("\nGET POSITION:");
    GPS.getPosition();
    //USB.print("Latitude (degrees):");
    lat = GPS.convert2Degrees(GPS.latitude, GPS.NS_indicator);
    //USB.println(lat);
    //USB.print("Longitude (degrees):");
    longi = GPS.convert2Degrees(GPS.longitude, GPS.EW_indicator);
    //USB.println(longi);
  }
  serialFlush(1);*/
  /*
  Utils.setMuxAux2();
  //_baudRate = 115200;
  beginSerial(115200,2);
  delay(50);
   serialFlush(2);
   //printString("hol\n", 2);
   //sprintf(send_buffer, "lat %d.%05d\n", lat);
   memset(send_buffer, 0x00, sizeof(send_buffer));
   memset(buffer2, 0x00, sizeof(buffer2));
   dtostrf(lat, 4, 8, buffer2);
   sprintf(send_buffer,"lat %s\n", buffer2);
  // printString("lat ", 2);
   printString(send_buffer, 2);
   i = 0;
   while(serialAvailable(2) > 0){
    x_string[i] = serialRead(2);
    i++;
   }
    USB.print(F("\n")); 
    USB.printf(x_string);
     memset(x_string, 0x00, sizeof(x_string));
   memset(send_buffer, 0x00, sizeof(send_buffer));
   memset(buffer2, 0x00, sizeof(buffer2));
   //sprintf(send_buffer, "long %d.%05d\n",longi);
   dtostrf(longi, 4, 8, buffer2);
   sprintf(send_buffer,"long %s\n", buffer2);
   //printString("long ", 2);
   printString(send_buffer, 2);
   i = 0;
   while(serialAvailable(2) > 0){
    x_string[i] = serialRead(2);
    i++;
   }
    USB.print(F("\n")); 
    USB.printf(x_string);
    memset(x_string, 0x00, sizeof(x_string));
    delay(100);*/


  //delay(6000);
  
  GPS.begin();

    status = GPS.waitForSignal(TIMEOUT); 
  

  if( status == true){
    //USB.println("\nGET POSITION:");
    GPS.getPosition();
    //USB.print("Latitude (degrees):");
    lat = GPS.convert2Degrees(GPS.latitude, GPS.NS_indicator);
    //USB.println(lat);
    //USB.print("Longitude (degrees):");
    longi = GPS.convert2Degrees(GPS.longitude, GPS.EW_indicator);
    //USB.println(longi);
  }
   digitalWrite(DIGITAL5, HIGH);

  Utils.setMuxAux2();
  //_baudRate = 115200;
  beginSerial(115200,2);
  delay(50);
          //delay(100);
       // serialFlush(2);
        //printString("FIRST MESSSAGE\n", 2);


  unsigned long waitStart = millis();

  while (true) {

    
    now = millis();

    if(serialAvailable(2) > 0) {
        char x = serialRead(2);

        //buffer[index++] = x;
        //USB.print(F("GABRIEL MESSAGE: "));
       // USB.println(x);
        
        if(x == 's') {

            USB.println("send");
            //delay(100);
            serialFlush(2);
                //memset(send_buffer, 0x00, sizeof(send_buffer));
                //memset(buffer2, 0x00, sizeof(buffer2));
      //  memset(buffer3, 0x00, sizeof(buffer3));
            dtostrf(lat, 4, 8, buffer2);
       // dtostrf(longi, 4, 8, buffer3);
            sprintf(send_buffer,"lat %s ", buffer2);
  
            printString(send_buffer, 2);
            
            
            //delay(700);
            serialFlush(2);
   //memset(send_buffer, 0x00, sizeof(send_buffer));
   //memset(buffer2, 0x00, sizeof(buffer2));
   dtostrf(longi, 4, 8, buffer2);
   sprintf(send_buffer,"long %s\n", buffer2);
   printString(send_buffer, 2);
    digitalWrite(DIGITAL5, LOW);
            break;
            
        } else {
            
        }
    }

    if(now - waitStart > WAIT) {
        //USB.println("TIMEOUT");
        //printString("wasp timed out\n", 2);
         digitalWrite(DIGITAL5, LOW);
        break;
    }

    
  }
   digitalWrite(DIGITAL5, LOW);


  //delay(100);

}
