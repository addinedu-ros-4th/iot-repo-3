/*
 * History
 * #240307 
 *  - if button is pressed, the barcode module starts scanning.
 *  - esp8266 sends "barcode value" to mqtt server
 *  
 * #240308
 *  - add server signal, and 
 */
#include <ESP8266WiFi.h>

// test
#define BTN D0
#define GLED D1
#define RLED D2
bool flg_btn = 0;

// mqtt
#include "PubSubClient.h"
// Update these with values suitable for your network.
const char* ssid = "AIE_509_2.4G";
const char* password = "addinedu_class1";
//const char* mqtt_server = "broker.mqtt-dashboard.com";
const char* mqtt_server = "192.168.0.85";
const int mqttPort = 1883;
#define outTopicOn "arduino1/outTopicOn"
#define outTopicBar "arduino1/outTopicBar"
#define inTopicStart "arduino1/inTopicStart"
#define inTopicMode "arduino1/inTopicMode"

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

//TX
int sigOperation = 0;

//RX
//int sigEmergency = 0;
int flgCallback = 0;
int sigServerCmd = 0;
// 0 : suspend
// 1 : operation
int sigConvMode = 0;
// 0 : ready(green led)
// 1 : move(red led)

bool flgStart = 0;

// barcode
#include "SoftwareSerial.h"
SoftwareSerial GM65Serial(14,12);   // MCU(RX,TX) - (SCK,MISO)
bool flgBarcode = 0;


float currentTime = 0;
float lastTime = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  flgCallback = 1;
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  #if 0
  if (topic == inTopicStart)
  {
    //a = (char)payload;
    sigServerCmd = payload - '0';
  }
  else if (topic == inTopicMode)
  {
    //b = (char)payload;
    sigConvMode = payload - '0';
  }
  else
  {
    //
  }
  #endif


  // test code
  #if 0
  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }
  #endif

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish(outTopicBar, "hello world");
      // ... and resubscribe
      client.subscribe(inTopicStart);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  // put your setup code here, to run once:
  
  
  Serial.begin(9600);
  //Serial.begin(115200);
  // MQTT
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  setup_wifi();
  client.setServer(mqtt_server, mqttPort);
  client.setCallback(callback);

  // barcode
  GM65Serial.begin(9600);   // GM65-아두이노간 통신, 9600은 공장출하초기값(변경가능)

  // test
  pinMode(BTN,INPUT);
  pinMode(GLED,OUTPUT);
  digitalWrite(GLED, LOW);

  Serial.println("Reset complete!");
}


void loop() 
{
  // put your main code here, to run repeatedly:

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // ######################################
  #if 1
  if (flgCallback == 0)
  {
    sigOperation = 1;
    String buf = String(sigOperation);
    char bufOp[50];
    buf.toCharArray(bufOp, 50);
    Serial.print("Publish message: ");
    Serial.println(bufOp);
    client.publish(outTopicOn, bufOp);

  }
  else if (flgCallback == 1)
  {
    // aleady operating....
  }
  else
  {
    // error
  }


  if (sigServerCmd == 1) flgStart = 1;
  else if (sigServerCmd == 0) flgStart = 0;
  else ; // Serial.print(command error);


  if (flgStart == 1)
  {
    if (sigConvMode == 0)
    {
      // ready mode
      digitalWrite(GLED, HIGH);
      digitalWrite(RLED, LOW);

      if ((currentTime - lastTime) > 1000)
      {
        flgBarcode = 1;
        lastTime = currentTime;
      }
      else
      {
        currentTime = millis();
        //
      }
    
      if (flgBarcode == 1)
      {
        String barcodeValue = BarcodeScan();
        char buf[50];
        barcodeValue.toCharArray(buf, 50);
    
        Serial.print("Publish message: ");
        Serial.println(buf);
        client.publish(outTopicBar, buf);
        //client.publish(outTopicBar, "XX04LI01");
    
        flgBarcode = 0;
      }
      else
      {
        //
      }
      
    }
    else if (sigConvMode == 1)
    {
      // move mode
      digitalWrite(GLED, LOW);
      digitalWrite(RLED, HIGH);
    }
    else ; // Serial.print(command error);
  }
  else
  {
    // suspend
  }

  #endif
  // ######################################

  
  
}

String BarcodeScan()
{
  byte gm65Cmd[] = {0x7E, 0x00, 0x08, 0x01, 0x00, 0x02, 0x01, 0xAB, 0xCD};
  GM65Serial.write(gm65Cmd, sizeof(gm65Cmd));
  
  // \n(Enter) 값들어오기 전까지 배열에 값 저장
  String strBarcode = GM65Serial.readStringUntil('\n');
  strBarcode = strBarcode.substring(7);

  return strBarcode;
}
