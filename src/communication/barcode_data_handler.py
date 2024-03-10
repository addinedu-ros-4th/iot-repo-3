import paho.mqtt.client as mqtt
import json
import sys
import os
sys.path.append(os.path.abspath('/home/addinedu/git_ws/iot-repo-3/src/communication/database'))
from communication.database.db_control import insert_database   # database control module
from datetime import datetime
from communication.serial_communication import write_serial_data


# ip_number = '192.168.219.108'           # house
ip_number = '192.168.0.85'                # edu


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
    
    # Insert Database
    split_insert(msg)


# For insert Database, split number
def split_insert(msg):
    barcode = msg.payload.decode('utf-8')
    print(f"Data : {barcode}")
    
    # barcode full_number slice
    size_category = barcode[:2]
    hub_name = barcode[2:4]
    treatment = barcode[4:6]
    
    start_time = datetime.now()
    
    insert_database(barcode, size_category, hub_name, treatment, start_time)
    
    # Send to Arduino board2 (serial communication) 'HubInfo'
    write_serial_data(hub_name)
    

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect           # callback definition setting
client.on_disconnect = on_disconnect     # callback definition setting
client.on_message = on_message           # callback definition setting

client.connect(ip_number, 1883, 60)      # MQTT brokcer IP
client.loop_forever()
