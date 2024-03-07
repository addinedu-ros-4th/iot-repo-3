import paho.mqtt.client as mqtt
import json

# Connecting broker callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("arduino1/outTopic")


# Disconnecting
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


# Subcriber callback
def on_message(client, userdata, msg):
    barcode = str(msg.payload)
    
    print(msg.topic + " -> " + str(msg.payload))
    

client = mqtt.Client()
client.on_connect = on_connect           # callback definition setting
client.on_disconnect = on_disconnect     # callback definition setting
client.on_message = on_message           # callback definition setting

client.connect("192.168.0.85", 1883, 60) # MQTT brokcer IP
client.loop_forever()
