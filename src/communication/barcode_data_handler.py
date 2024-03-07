import paho.mqtt.client as mqtt
from database.insert_db import insert_database
import json

ip_number = '192.168.219.108'           # house
# ip_number = '192.168.0.85'            # edu


# Connecting broker callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("arduino1/outTopic")


# Disconnecting broker callback
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


# Subcriber callback
def on_message(client, userdata, msg):
    topic_name = msg.topic
    print(f"Topic : {topic_name}")
    
    split_number(msg)


# For insert Database, split number
def split_number(msg):
    barcode_number = msg.payload.decode('utf-8')
    print(f"Data : {barcode_number}")
    
    # barcode full_number slice
    category = barcode_number[:2]
    hub_name = barcode_number[2:4]
    state = barcode_number[4:6]
    
    insert_database(barcode_number, category, hub_name, state)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect           # callback definition setting
client.on_disconnect = on_disconnect     # callback definition setting
client.on_message = on_message           # callback definition setting

client.connect(ip_number, 1883, 60)      # MQTT brokcer IP
client.loop_forever()
