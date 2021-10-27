#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <WiFi.h>
#include <WiFiUdp.h>

const char * ssid = "OpenWrt"; //ROG   ROG-NET
const char * pwd = "";
// IP address to send UDP data to.
// it can be ip address of the server or
// a network broadcast address
// here is broadcast address

const char * udpAddress = "192.168.1.152";    //100, 101, 102,103, 110, 120, 130, 140,150
const int udpPort = 8888;  //E=9999,D=8888,C=7777,B=6666,A=5555,g=4444,n=3333

char qw[255],qx[255], qy[255], qz[255],qroll[255], qpitch[255], qyaw[255],roll[255], pitch[255], yaw[255], accx[255], accy[255], accz[255], gyrx[255], gyry[255], gyrz[255], Mx[255], My[255], Mz[255],gravaccx[255],gravaccy[255],gravaccz[255];

unsigned long timer=0;
unsigned long counter = 0;
int hs = 0;
int distance = 0;
WiFiUDP udp;
/* Returns the IMU data as both a euler angles and quaternions as the WebSerial
   3D Model viewer at https://adafruit-3dmodel-viewer.glitch.me/ expects.
 
   This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2020/JUN/01  - First release (Melissa LeBlanc-Williams)
*/
/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x29);

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  //Serial.begin(9600);
  Serial.println("WebSerial 3D Firmware"); Serial.println("");

  Wire.begin(21, 22, 400000); // (SDA, SCL) (21, 22) are default on ESP32, 400 kHz I2C bus speed
  delay(5000);
  
 //pinMode(13,INPUT);
 
 WiFi.begin(ssid, pwd);
 Serial.println(WiFi.localIP());
 udp.begin(udpPort);

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
   
  delay(1000);

  /* Use external crystal for better accuracy */
  bno.setExtCrystalUse(true);
   
  /* Display some basic information on this sensor */
  displaySensorDetails();
  
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Board layout:
         +----------+
         |         *| RST   PITCH  ROLL  HEADING
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+
  */
 

  /* The WebSerial 3D Model Viewer expects data as heading, pitch, roll */
  Serial.print(F("Orientation: "));
  Serial.print(360 - (float)event.orientation.x);
  Serial.print(F(", "));
  Serial.print((float)event.orientation.y);
  Serial.print(F(", "));
  Serial.print((float)event.orientation.z);
  Serial.println(F(""));

  float Yaw = 360 - (float)event.orientation.x;
  float Pitch = (float)event.orientation.y;
  float Roll = (float)event.orientation.z;

    imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  float accX = (float)acc.x();
  float accY = (float)acc.y();
  float accZ = (float)acc.z();

  Serial.print("Aceelremote:");
  Serial.print(accX);
  Serial.print(F(", "));
  Serial.print(accY);
  Serial.print(F(", "));
  Serial.print(accZ);

  imu::Vector<3> gravacc = bno.getVector(Adafruit_BNO055::VECTOR_GRAVITY);
  float gravaccX = (float)gravacc.x();
  float gravaccY = (float)gravacc.y();
  float gravaccZ = (float)gravacc.z();

  Serial.print("GravityAceelremote:");
  Serial.print(gravaccX);
  Serial.print(F(", "));
  Serial.print(gravaccY);
  Serial.print(F(", "));
  Serial.print(gravaccZ);


    imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  float gyroX = (float)gyr.x();
  float gyroY = (float)gyr.y();
  float gyroZ = (float)gyr.z();

//  Serial.print("gyroote:");
//  Serial.print(gyroX);
//  Serial.print(F(", "));
//  Serial.print(gyroY);
//  Serial.print(F(", "));
//  Serial.print(gyroZ);

  imu::Quaternion quat = bno.getQuat();
  float q0 = (float)quat.w();
  float q1 = (float)quat.x();
  float q2 = (float)quat.y();
  float q3 = (float)quat.z();

    float QYaw   = atan2(2.0f * (q1 * q2 + q0 * q3), q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3);  
    float QPitch = -asin(2.0f * (q1 * q3 - q0 * q2));
    float QRoll  = atan2(2.0f * (q0 * q1 + q2 * q3), q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3);
    
    QPitch *= 180.0f / PI;
    QYaw   *= 180.0f / PI;
    QRoll  *= 180.0f / PI;

    dtostrf(Yaw, 3, 2, yaw);
    dtostrf(Pitch, 3, 2, pitch);
    dtostrf(Roll, 3, 2, roll);
    dtostrf(QYaw, 3, 2, qyaw);
    dtostrf(QPitch, 3, 2, qpitch);
    dtostrf(QRoll, 3, 2, qroll);
    dtostrf(q0, 3, 2, qw);
    dtostrf(q1, 3, 2, qx);
    dtostrf(q2, 3, 2, qy);
    dtostrf(q3, 3, 2, qz);
    dtostrf(accX, 3, 2, accx);
    dtostrf(accY, 3, 2, accy);
    dtostrf(accZ, 3, 2, accz);
    dtostrf(gyroX, 3, 2, gyrx);
    dtostrf(gyroY, 3, 2, gyry);
    dtostrf(gyroZ, 3, 2, gyrz);
    dtostrf(gravaccX, 3, 2, gravaccx);
    dtostrf(gravaccY, 3, 2, gravaccy);
    dtostrf(gravaccZ, 3, 2, gravaccz);
    counter++;

    
  timer =millis();

udp.beginPacket(udpAddress, udpPort);
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();   

    udp.beginPacket("192.168.1.101", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();

    udp.beginPacket("192.168.1.102", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();   

    udp.beginPacket("192.168.1.103", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();

    udp.beginPacket("192.168.1.152", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();    

    udp.beginPacket("192.168.1.120", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.130", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.152", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();

    udp.beginPacket("192.168.1.150", udpPort); //NTP requests are to port 123
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gyrx);      //3
    udp.print(',');
    udp.print(gyry);      //4
    udp.print(',');
    udp.print(gyrz);      //5
    udp.print(',');
    udp.print(qw);        //6
    udp.print(',');
    udp.print(qx);        //7
    udp.print(',');
    udp.print(qy);        //8
    udp.print(',');
    udp.print(qz);        //9  
    udp.print(',');
    udp.print(qyaw);      //10    -13
    udp.print(',');
    udp.print(qpitch);    //11    -12
    udp.print(',');
    udp.print(qroll);     //12    -11
    udp.print(',');
    udp.print(yaw);       //13    -10
    udp.print(',');
    udp.print(pitch);     //14    -9
    udp.print(',');
    udp.print(roll);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(hs);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();  

  /* The WebSerial 3D Model Viewer also expects data as roll, pitch, heading */
  
  
  Serial.print(F("Quaternion: "));
  Serial.print((float)quat.w());
  Serial.print(F(", "));
  Serial.print((float)quat.x());
  Serial.print(F(", "));
  Serial.print((float)quat.y());
  Serial.print(F(", "));
  Serial.print((float)quat.z());
  Serial.println(F(""));

  /* Also send calibration data for each sensor. */
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(F("Calibration: "));
  Serial.print(sys, DEC);
  Serial.print(F(", "));
  Serial.print(gyro, DEC);
  Serial.print(F(", "));
  Serial.print(accel, DEC);
  Serial.print(F(", "));
  Serial.print(mag, DEC);
  Serial.println(F(""));

//  delay(BNO055_SAMPLERATE_DELAY_MS);
}
