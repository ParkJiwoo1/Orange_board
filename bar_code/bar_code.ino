

#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3);

String str = "";
String msg = "";
int hour = 0, minute = 0, second = 0;
int day = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  mySerial.begin(9600);
}

void loop()
{

  if (mySerial.available())
  {
    str = mySerial.readString();
    Serial.println(str);
  }
  if (Serial.available())
  {
    msg = Serial.readStringUntil('\n');

    if (msg.indexOf("on") > -1)
    {
      digitalWrite(4, HIGH);
    }
    if (msg.indexOf("off") > -1)
    {
      digitalWrite(4, LOW);
    }
  }
}
