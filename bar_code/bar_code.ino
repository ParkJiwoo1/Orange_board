

#include <SoftwareSerial.h> // 시리얼 포트가 부족한 경우, 다른 기기와 시리얼 통신을 위한 아두이노 라이브러리

SoftwareSerial mySerial(2, 3); // RX, TX

String str = ""; //시리얼수신 문자열 저장
String msg = "";
int hour = 0, minute = 0, second = 0; // 시, 분, 초
int day = 0;                          // day

void setup()
{
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  mySerial.begin(9600);
}

void loop()
{
  // lcd.print("Orange !");
  //  available문 안에서 동시 확인
  if (mySerial.available())
  {
    str = mySerial.readString(); // read()가 아닌 readString()으로 읽기 :: 문자열로 읽기
                                 //왜? 웬만한 교과서에는 read()로 한 문자만 읽어오는 것만 설명하는지 모르겠음
    // str = str.substring(0, str.length() - 3); //시리얼모니터에서 엔터 치면서 마지막에 송신한 '\n' 제거
    Serial.println(str); // 수신 데이터 확인
                         // Serial.print("--------( ");                // 구분선
                         // Serial.print(str.length());              // 수신 받은 문자열 길이 확인
                         // Serial.print(" )--------// ");              // 구분선
    // lcd.clear();
    // lcd.print("Orange!");
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
