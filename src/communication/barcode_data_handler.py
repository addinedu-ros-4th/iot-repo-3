import paho.mqtt.client as mqtt
import json
import sys
from database.insert_db import insert_database
from datetime import datetime


# ip_number = '192.168.219.108'           # house
ip_number = '192.168.0.85'            # edu


# Connecting broker callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("arduino1/outTopicBar")


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
    barcode = msg.payload.decode('utf-8')
    print(f"Data : {barcode}")
    
    # barcode full_number slice
    size_category = barcode[:2]
    hub_name = barcode[2:4]
    treatment = barcode[4:6]
    
    start_time = datetime.now()
    
    insert_database(barcode, size_category, hub_name, treatment, start_time)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect           # callback definition setting
client.on_disconnect = on_disconnect     # callback definition setting
client.on_message = on_message           # callback definition setting

client.connect(ip_number, 1883, 60)      # MQTT brokcer IP
client.loop_forever()
