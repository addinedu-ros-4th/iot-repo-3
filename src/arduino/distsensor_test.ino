int sensorValue1;
int sensorValue2;
int sensorValue3;
int sensorValue4;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);   
}

void loop() {
  // put your main code here, to run repeatedly:
    sensorValue1 = analogRead(A0);
    sensorValue2 = analogRead(A1);
    sensorValue3 = analogRead(A2);
    sensorValue4 = analogRead(A3);

    Serial.print("1:");
    Serial.println(sensorValue1);
    Serial.print("2:");
    Serial.println(sensorValue2);
    Serial.print("3:");
    Serial.println(sensorValue3);
    Serial.print("4:");
    Serial.println(sensorValue4);

    delay(10);
}