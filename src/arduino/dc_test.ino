#include <Servo.h>
#include <Arduino.h>

String tmpReceiveString;


int ENA = 9; // PWM 제어 핀
int IN1 = 10; // 모터 회전 방향 제어 핀 1
int IN2 = 11; // 모터 회전 방향 제어 핀 2

int ENA_2 = 5; // PWM 제어 핀
int IN1_2 = 6; // 모터 회전 방향 제어 핀 1
int IN2_2 = 7; // 모터 회전 방향 제어 핀 2

void setup() {
  // put your setup code here, to run once:
    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);

    pinMode(ENA_2, OUTPUT);
    pinMode(IN1_2, OUTPUT);
    pinMode(IN2_2, OUTPUT);
    }

    void loop() {
    // put your main code here, to run repeatedly:
    if(Serial.available() >0)
    {
        // Serial.println("---");
        String inputStr = Serial.readStringUntil('\n');
        //Serial.println(inputStr);
        tmpReceiveString = inputStr;

    }

    if (tmpReceiveString != "")
        {
        if (tmpReceiveString == '1')
        {
            analogWrite(ENA, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
            digitalWrite(IN1, LOW); // 모터 회전 방향 설정
            digitalWrite(IN2, LOW);
            analogWrite(ENA_2, 0); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
            digitalWrite(IN1_2, LOW); // 모터 회전 방향 설정
            digitalWrite(IN2_2, LOW);
            
        }

        if (tmpReceiveString == '2')
        {
            analogWrite(ENA, 60); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
            digitalWrite(IN1, HIGH); // 모터 회전 방향 설정
            digitalWrite(IN2, LOW);
            analogWrite(ENA_2, 60); // 속도 조절을 위한 PWM 신호 (0-255 사이의 값)
            digitalWrite(IN1_2, HIGH); // 모터 회전 방향 설정
            digitalWrite(IN2_2, LOW);
            
        }
        }


}