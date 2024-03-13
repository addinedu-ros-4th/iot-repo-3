#include <Servo.h>
#include <Arduino.h>

#define CONVEYORVEL 60
Servo servo1;
Servo servo2;
Servo servo3;

int ENA = 9; // PWM 제어 핀
int IN1 = 10; // 모터 회전 방향 제어 핀 1
int IN2 = 11; // 모터 회전 방향 제어 핀 2

int ENA_2 = 5; // PWM 제어 핀
int IN1_2 = 6; // 모터 회전 방향 제어 핀 1
int IN2_2 = 7; // 모터 회전 방향 제어 핀 2

const int totalservoNum = 3;
const int totaldistSensorNum = 4;
const int emgbuttonPin = 12;
const int servoPin[totalservoNum] = {2,3,4};
const int servoangleWait[totalservoNum] = {170,0,170};
const int servoangleBlock[totalservoNum] = {90,90,90};
const int servoangleThrow[totalservoNum] = {170,0,170};

const int distSensorPin[totaldistSensorNum] = {A0,A1,A2,A3};
const int sensorDistanceLimit[totaldistSensorNum] = {300,300,300,300};
int distSensorStatus[totaldistSensorNum] = {0, 0, 0, 0};


int numHub = 0;
int step = 0;
int servotimer = 0;
const int servotimerlimit = 300;

int statusconveyor =0;//0: 구동하지 않음 1: 구동 중 
int statusworking =0;
int isunkownhub =0;
int unknowntimer =0;
int isemg = 0;
int emgbuttonState = HIGH;
int prevemgbuttonState = LOW;

//bosun merge
//

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  servo1.attach(servoPin[0]);
  servo1.write(servoangleWait[0]);

  servo2.attach(servoPin[1]);
  servo2.write(servoangleWait[1]);

  servo3.attach(servoPin[2]);
  servo3.write(servoangleWait[2]);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENA_2, OUTPUT);
  pinMode(IN1_2, OUTPUT);
  pinMode(IN2_2, OUTPUT);

}

void distSensorCheck()
{
  int sensorValue;

  for (int i=0; i<totaldistSensorNum; i++)
  {
    sensorValue = analogRead(distSensorPin[i]);
    if(sensorValue > sensorDistanceLimit[i])
    {
      distSensorStatus[i] = 1;
    }
    else
    {
      distSensorStatus[i] = 0;
    }
  }

}

void conveyorRun()
{
  if (numHub == 0)
  {
    //이미 conveyor가 구동 중인지 확인
    if(statusconveyor == 1)//conveyor 가 돌고 있는지 확인 할 수 있는 코드
    {
      statusconveyor =0;
      //Serial.println("conveyor 정지");
    }
    else
    {
      //
    }
  }
  else
  {
    if(statusconveyor == 1) //conveyor가 돌고 있는지 확인 할 수 있는 코드
    {
      //돌고 있으면 
      
    }
    else
    {
      statusconveyor =1;
      //Serial.println("conveyor 구동");
    }
  }

  if(statusconveyor == 1)
  {
    if(isemg == 0)
    {
      analogWrite(ENA, CONVEYORVEL); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1, HIGH); // 모터 회전 방향 설정
      digitalWrite(IN2, LOW);
      analogWrite(ENA_2, CONVEYORVEL); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1_2, HIGH); // 모터 회전 방향 설정
      digitalWrite(IN2_2, LOW);
    }
    else
    {
      analogWrite(ENA, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1, LOW); // 모터 회전 방향 설정
      digitalWrite(IN2, LOW);
      analogWrite(ENA_2, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1_2, LOW); // 모터 회전 방향 설정
      digitalWrite(IN2_2, LOW);
    }
  }
  else
  {
    if (isunkownhub == 1 )
    {
      if(unknowntimer == 1000)
      {
        unknowntimer = 0;
        isunkownhub =0;
      }
      else
      {
        if(isemg == 0)
        {
          analogWrite(ENA, CONVEYORVEL); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
          digitalWrite(IN1, HIGH); // 모터 회전 방향 설정
          digitalWrite(IN2, LOW);
          analogWrite(ENA_2, CONVEYORVEL); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
          digitalWrite(IN1_2, HIGH); // 모터 회전 방향 설정
          digitalWrite(IN2_2, LOW);
          unknowntimer++;
        }
        else
        {
          analogWrite(ENA, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
          digitalWrite(IN1, LOW); // 모터 회전 방향 설정
          digitalWrite(IN2, LOW);
          analogWrite(ENA_2, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
          digitalWrite(IN1_2, LOW); // 모터 회전 방향 설정
          digitalWrite(IN2_2, LOW);
        }
      }
    }
    else
    {
      analogWrite(ENA, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1, LOW); // 모터 회전 방향 설정
      digitalWrite(IN2, LOW);
      analogWrite(ENA_2, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
      digitalWrite(IN1_2, LOW); // 모터 회전 방향 설정
      digitalWrite(IN2_2, LOW);
    }

    
  }
}

void receiveSerial()
{
  String tmpReceiveString;

  while(Serial.available() >0)
  {
    // Serial.println("---");
    String inputStr = Serial.readStringUntil('\n');
    //Serial.println(inputStr);
    tmpReceiveString = inputStr;

  }

  if(numHub == 0)
  {
    if (tmpReceiveString != "")
    {
      if ((tmpReceiveString[0] == '#') && (tmpReceiveString[tmpReceiveString.length()-1] == '#') && (tmpReceiveString.length() == 10))
      {
      //  Serial.print("HUB :");
      //  Serial.println(tmpReceiveString.substring(7,9));
      
        numHub = tmpReceiveString.substring(7,9).toInt();
        statusworking =1;
        
      }
      else if ((tmpReceiveString[0] == '#') && (tmpReceiveString[tmpReceiveString.length()-1] == '#') && (tmpReceiveString.length() == 11))
      {
        if ((tmpReceiveString.charAt(3) == 'E') && (tmpReceiveString.charAt(4) == 'M') && (tmpReceiveString.charAt(5) == 'G'))
        {
          //emg stop : only dc stop
          isemg = 1;
          sendToServer(1);
          
        } 
      }
      else if ((tmpReceiveString[0] == '#') && (tmpReceiveString[tmpReceiveString.length()-1] == '#') && (tmpReceiveString.length() == 9))
      {
        if ((tmpReceiveString.charAt(3) == 'S') && (tmpReceiveString.charAt(4) == 'T') && (tmpReceiveString.charAt(5) == 'A'))
        {
          //start
          isemg = 0;
        } 
      }  
    }
  }
}

void servoCheck()
{
  if(numHub == 0)
  {
    return;
  }
  else if(isemg == 1)
  {
    return;
  }
  else
  {
    if((1<=numHub) && (numHub <= 3))
    {
      servoWrite(numHub);
    }
    else //hub doesn't exist
    {
      if (distSensorStatus[3] == 1)// 마지막 입구에서 인식 되면
      {
        sendToServer(0);
        numHub =0;
        isunkownhub = 1;
      }
    }
  }
}

void servoWrite(int hub)
{ 
  //Serial.println(step);
  hub = hub -1; //array std
  //Serial.println(distSensorStatus[hub]);
  if (step == 0 )
  {
    if (hub == 0)// 허브 1번
    {
      servo1.write(servoangleBlock[hub]);
      step++;
    }
    else if (hub ==1) // 허브 2번
    {
      servo2.write(servoangleBlock[hub]);
      step++;
    }
    else if (hub  == 2) //허브 3번
    {
      servo3.write(servoangleBlock[hub]);
      step++;
    }
    else
    {
      //Serial.println("not here");
    }
    
  }
  else if (step == 1)
  {
    if (distSensorStatus[hub] == 1)
    {
      if (hub == 0)
      {
        servo1.write(servoangleThrow[hub]);
        step++;
      }
      else if (hub == 1)
      {
        servo2.write(servoangleThrow[hub]);
        step++;
      }
      else if (hub  == 2)
      {
        servo3.write(servoangleThrow[hub]);
        step++;
      }
      else
      {
        
      }
    }
  }
  else if (step == 2)
  {
    if (servotimer == servotimerlimit)
    {
      if (hub == 0)
      {
        servo1.write(servoangleWait[hub]);
        sendToServer(0);
        step =0;
        numHub =0;
      }
      else if (hub ==1)
      {
        servo2.write(servoangleWait[hub]);
        sendToServer(0);
        step =0;
        numHub =0;
      }
      else if (hub == 2)
      {
        servo3.write(servoangleWait[hub]);
        sendToServer(0);
        step =0;
        numHub =0;
      }

      servotimer =0;
    }
    else
    {
      servotimer++;
    }
  
  }
  else
  {
    step =0;

  }
}

void sendToServer(int tmpflag)
{
  //tmpflag : 
  //0: send STATEDONE, 1: EMGDONE

  String tmpstr = "";
  String sendresultStr = "";
  String sendStr = "#B2@";

  if(tmpflag == 0)
  {
    tmpstr = "STATE";
    sendresultStr = sendStr + tmpstr+"DONE#"; 
  }
  else if(tmpflag == 1)
  {
    tmpstr = "EMG";
    sendresultStr = sendStr + tmpstr+"DONE#";
  }

  for(int i=0; i<sendresultStr.length(); i++)
    {
      Serial.print(sendresultStr[i]);
    }
  
}

void emgbuttonRead()
{
  emgbuttonState = digitalRead(emgbuttonPin);
}

void emgbuttonPresscheck()
{
  if(prevemgbuttonState == LOW)
  {
    if(emgbuttonState == HIGH)
    {
      if(isemg == 1)
      {
        isemg = 0;
      }
      else
      {
        isemg = 1;
      }
    }
  }
  prevemgbuttonState = emgbuttonState;
}

void loop() {
  // put your main code here, to run repeatedly:
  receiveSerial();
  distSensorCheck();
  emgbuttonRead();
  emgbuttonPresscheck();
  conveyorRun();
  receiveSerial();
  servoCheck();
  delay(1);
  

}