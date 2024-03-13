/*
 * History
 * #240307 
 *  - if button is pressed, the barcode module starts scanning.
 *  - esp8266 sends "barcode value" to mqtt server
 *  
 * #240308
 *  - add server signal
 *  
 * #240312_1
 *  - 1st test complete
 * 
 * #240312_2
 *  - final code diet!
 *  
 * #240313
 *  - Add green LED for recognize barcode reading success
 */
#include <ESP8266WiFi.h>

float lastTime = millis();

// mqtt
#include <PubSubClient.h>// Update these with values suitable for your network.
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

// barcode
#include <SoftwareSerial.h>
SoftwareSerial GM65Serial(14,12);   // MCU(RX,TX) - (SCK,MISO)

// LED
#define GLED D3


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
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

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
      //client.publish(outTopicBar, "Board1 Connected!");
      // ... and resubscribe
      client.subscribe(inTopicStart);
      client.subscribe(inTopicMode);
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
  // MQTT
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  setup_wifi();
  client.setServer(mqtt_server, mqttPort);
  client.setCallback(callback);

  // barcode
  GM65Serial.begin(9600);   // GM65 Module factory default baudrate

  // LED
  pinMode(GLED, OUTPUT);

  Serial.println("Reset complete!");
}


void loop() 
{
  // put your main code here, to run repeatedly:

  if (!client.connected()) {
    reconnect();
  }
  client.loop();


  // 2 sec period mode
  #if 1
  if ((millis() - lastTime) > 2000)
  {
    digitalWrite(GLED, LOW);
    String barcodeValue = BarcodeScan();    
    char buf[50];
    barcodeValue.toCharArray(buf, 50);

    if (int(buf[0]) == 0)
    {
      //Serial.println("Null");
    }
    else if (buf[7] == 0)
    {
      //Serial.println("data loss");
    }
    else
    {
      digitalWrite(GLED, HIGH);
      //Serial.print("Publish message: ");
      //Serial.println(buf);
      client.publish(outTopicBar, buf);
    }
    lastTime = millis();
  }
  else
  {
    //
  }
  #endif
  
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
