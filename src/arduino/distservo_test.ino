#include <Servo.h>
#include <Arduino.h>

Servo servo1;
Servo servo2;
Servo servo3;

String recstr;

int servo1angle =0;
int servo2angle =180;
int servo3angle =0;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    servo1.attach(2);
    servo1.write(servo1angle);

    servo2.attach(3);
    servo2.write(servo2angle);

    servo3.attach(4);
    servo3.write(servo3angle);
}

void loop() {
  // put your main code here, to run repeatedly:
    if(Serial.available()>0)
    {
        recstr = Serial.readStringUntil('\n');
    }

    if(recstr == '1')
    {
        servo1angle += 10;
        //servo1angle -= 10;

    }
    else if(recstr == '2')
    {
        servo2angle += 10;
        //servo2angle -= 10;

    }
    else if(recstr == '3')
    {
        servo3angle += 10;
        //servo3angle -= 10;

    }
    }