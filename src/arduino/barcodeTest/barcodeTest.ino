#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>

#define GLED D0
#define BTN D1


bool flg_btn = 0;

SoftwareSerial GM65Serial(14,12);   // MCU(RX,TX) - (SCK,MISO)

void setup() {
  // put your setup code here, to run once:
  pinMode(BTN,INPUT);
  pinMode(GLED,OUTPUT);
  
  Serial.begin(9600);
  //Serial.begin(115200);
  GM65Serial.begin(9600);   // GM65-아두이노간 통신, 9600은 공장출하초기값(변경가능)

  Serial.println("Reset complete!");

  digitalWrite(GLED, LOW);
}


void loop() 
{
  // put your main code here, to run repeatedly:

  #if 1
  int btnState = digitalRead(BTN);
  //Serial.println(btnState);
  #endif

  #if 1
  if (btnState == HIGH)
  {
    //Serial.println(btnState);
    digitalWrite(GLED, HIGH);
    if (flg_btn == 0)
    {
      // 바코드 리드명령
      BarcodeScan();
      flg_btn = 1;
    }
    else
    {
      //nono
    }
  }
  else
  {
    flg_btn = 0;
    digitalWrite(GLED, LOW);
  }
  #endif
  
}


void BarcodeScan()
{
  byte gm65Cmd[] = {0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD};
  GM65Serial.write(gm65Cmd, sizeof(gm65Cmd));
  delay(500);
  
  // \n(Enter) 값들어오기 전까지 배열에 값 저장
  String barcode = GM65Serial.readStringUntil('\n');
  barcode = barcode.substring(7);
  Serial.println(barcode.length());
  Serial.println(barcode);
  
}
