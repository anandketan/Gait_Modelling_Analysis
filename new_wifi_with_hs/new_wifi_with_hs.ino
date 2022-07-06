#include <Wire.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const char * ssid = "ROG-NET"; //ROG   ROG-NET
const char * pwd = "network@";
// IP address to send UDP data to.
// it can be ip address of the server or
// a network broadcast address
// here is broadcast address

int sc = 0;

const char * udpAddress = "192.168.1.100";//100, 101, 102, 110, 120, 130, 140
const int udpPort = 5555;  //E=9999,D=8888,C=7777,B=6666,A=5555,g=4444,n=3333

unsigned long timer=0;
unsigned long counter = 0;

int buttonState=0;             // the current reading from the input pin
int lastButtonState = 0;
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 70;

WiFiUDP udp;
int LED = 2;
int buzzpin = 13; //TCK
long check;
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
float threshold = 0;
int avg = 0;
int hs = 0;

#define echoPin 14  //TMS
#define trigPin 15  //TDO

void setup(void)
{
  Serial.begin(115200);
  WiFi.begin(ssid, pwd);
  Serial.println(WiFi.localIP());
  udp.begin(udpPort);

  pinMode (LED, OUTPUT);
  pinMode (buzzpin, OUTPUT);

  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
  for(int i=0;i<=1000;i++)
  {
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      duration = pulseIn(echoPin, HIGH, 100000);
  // Calculating the distance
      distance = duration * 0.034 / 2;
      avg = avg + distance;
      threshold = avg/1000;
  }
    Serial.print(threshold);
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
//  check = pulseIn(echoPin, HIGH, 100000);
//  while(check > 0)
//  {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH, 20000);
  distance = duration * 0.034 / 2; 
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
//  }
 if (distance < 110)
{
  if (distance <= threshold)
  {
     hs = 1;
  }
  else
  {
    hs = 0;
  }


  if (hs != lastButtonState)
  {
//    Serial.println("hs");
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) 
  { 
    
    if (hs != buttonState) 
    {
      buttonState = hs;
      
      if (buttonState == 1) 
      {      
        digitalWrite(LED,HIGH);
        digitalWrite(buzzpin,HIGH);
        sc = 1;
      }
      else 
      {
        digitalWrite(LED,LOW);
        digitalWrite(buzzpin,LOW);
        sc=0;
      }
    }
  }
   lastButtonState = hs;
 }
  if(distance>100)
    distance=100;
    else
    distance=distance;
   counter++;
    
  timer =millis();

udp.beginPacket(udpAddress, udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket();   

    udp.beginPacket("192.168.1.101", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.102", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.103", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.110", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.120", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.130", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.140", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

    udp.beginPacket("192.168.1.150", udpPort); //NTP requests are to port 123
    udp.print(0);      //0
    udp.print(',');
    udp.print(0);      //1
    udp.print(',');
    udp.print(0);      //2
    udp.print(',');
    udp.print(0);      //3
    udp.print(',');
    udp.print(0);      //4
    udp.print(',');
    udp.print(0);      //5
    udp.print(',');
    udp.print(0);        //6
    udp.print(',');
    udp.print(0);        //7
    udp.print(',');
    udp.print(0);        //8
    udp.print(',');
    udp.print(0);        //9  
    udp.print(',');
    udp.print(0);      //10    -13
    udp.print(',');
    udp.print(0);    //11    -12
    udp.print(',');
    udp.print(0);     //12    -11
    udp.print(',');
    udp.print(0);       //13    -10
    udp.print(',');
    udp.print(0);     //14    -9
    udp.print(',');
    udp.print(0);      //15    -8
    udp.print(',');
    udp.print(counter);   //16    -7
    udp.print(','); 
    udp.print(timer);     //17    -6
    udp.print(',');
    udp.print(sc);        //18    -5
    udp.print(',');
    udp.print(distance);  //19    -4
    udp.print(',');
    udp.print(0);  //20    -3
    udp.print(',');
    udp.print(0);  //21    -2
    udp.print(',');
    udp.print(0);  //22    -1
    udp.endPacket(); 

}
