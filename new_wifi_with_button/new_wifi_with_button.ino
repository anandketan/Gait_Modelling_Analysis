#include <WiFi.h>
#include <WiFiUdp.h>

const char * ssid = "ROG-NET"; //ROG   ROG-NET
const char * pwd = "network@";


const char * udpAddress = "192.168.1.100";//100, 101, 102,103, 110, 120, 130, 140,150
const int udpPort = 9999;  //E=9999,D=8888,C=7777,B=6666,A=5555,g=4444,n=3333

unsigned long timer=0;
unsigned long counter = 0;

int sc = 0;
int distance = 0;

#define button 13

WiFiUDP udp;

void setup(void)
{
 //Serial.begin(115200);
 pinMode(13,INPUT);
 pinMode(12,OUTPUT);
 pinMode(02,OUTPUT);
 pinMode(14,OUTPUT);
 digitalWrite(12,HIGH);
 digitalWrite(14,LOW);
 WiFi.begin(ssid, pwd);
 //Serial.println(WiFi.localIP());
 udp.begin(udpPort);
}

void loop(void)
{    
  int val = digitalRead(button);
  if(val==HIGH){
    sc=1;
    digitalWrite(2,HIGH);
  }
  else{
    sc=0                                                                                                 ;
    digitalWrite(2,LOW);
    }    
  timer =millis();

udp.beginPacket(udpAddress, udpPort); //NTP requests are to port 123
    udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   

    udp.beginPacket("192.168.1.101", udpPort); //NTP requests are to port 123
    udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   

    udp.beginPacket("192.168.1.102", udpPort); //NTP requests are to port 123
        udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();     

    udp.beginPacket("192.168.1.103", udpPort); //NTP requests are to port 123
         udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   

    udp.beginPacket("192.168.1.110", udpPort); //NTP requests are to port 123
           udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();     

    udp.beginPacket("192.168.1.120", udpPort); //NTP requests are to port 123
           udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   

    udp.beginPacket("192.168.1.130", udpPort); //NTP requests are to port 123
    udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   
    
    udp.beginPacket("192.168.1.140", udpPort); //NTP requests are to port 123
          udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   

    udp.beginPacket("192.168.1.150", udpPort); //NTP requests are to port 123
          udp.print(0);//0
    udp.print(',');
    udp.print(0);//1
    udp.print(',');
    udp.print(0);//2
    udp.print(',');
    udp.print(0);//3
    udp.print(',');
    udp.print(0);//4
    udp.print(',');
    udp.print(0);//5
    udp.print(',');
    udp.print(0);//6
    udp.print(',');
    udp.print(0);//7
    udp.print(',');
    udp.print(0);//8
    udp.print(',');
    udp.print(0);//9  
    udp.print(',');
    udp.print(0);//10
    udp.print(',');
    udp.print(0);//11
    udp.print(',');
    udp.print(0);//12
    udp.print(',');
    udp.print(0);////13
    udp.print(',');
    udp.print(0);//14
    udp.print(',');
    udp.print(0);//-3//15
    udp.print(',');
    udp.print(0);//16
    udp.print(','); //NTP requests are to port 123
    udp.print(0);
    udp.print(',');
    udp.print(sc);
    udp.print(',');
    udp.print(distance);
    udp.endPacket();   
}
