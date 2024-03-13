import paho.mqtt.client as mqtt
import threading
import sys
import os
import time
from datetime import datetime
import serial

sys.path.append(os.path.abspath('/home/addinedu/git_ws/iot-repo-3/src/communication/database'))
from database.db_control import insert_database, change_state  # database control module

from motor_manager import MotorManager

inputs = []
isreturn = 0


# MQTT setting
ip_number = '192.168.0.85'               

# Serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=15)
data_save = ''


# Connecting broker callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("arduino1/outTopicBar")


# Subcriber callback
def on_message(client, userdata, msg):
    topic_name = msg.topic
    print(f"Topic : {topic_name}")
    
    # Insert Database
    barcode_process(msg)


def mqtt_client_thread():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect           # callback definition setting
    client.on_message = on_message           # callback definition setting

    client.connect(ip_number, 1883, 60)      # MQTT brokcer IP
    client.loop_forever()


def serial_thread():
    ser.flushInput()    # 시리얼 포트 비우기
    
    while True:
        if ser.readable(): #serial read
            tmpmsg = ser.read_until(size =14)
            signal = tmpmsg.decode('utf-8')
            
            if signal == '#B2@STATEDONE#':   # 분류 완료 시그널 수신
                change_state(data_save)
            time.sleep(3) # cpu 효율
                
        else:
            print("none")

            
def write_serial_data(data):
    if ser.isOpen():
        data_to_send = data if len(data) > 4 else "#S@HUB,{}#".format(data)
        print(f"Sending data : {data_to_send}")
        
        ser.write(bytes(data_to_send, "utf-8"))
        time.sleep(1)  # 데이터 전송 후 충분한 시간을 기다림
        print("Data sent successfully.")
                  
    else:
        print("Serial port is not open.")
        

# split data, insert database, write Arduino2 (serial)
def barcode_process(msg):
    global data_save
    
    barcode = msg.payload.decode('utf-8')
    data_save = barcode
    print(f"Data : {barcode}")
    
    # barcode full_number slice
    size_category = barcode[:2]
    hub_name = barcode[2:4]
    treatment = barcode[4:6]
    
    start_time = datetime.now()
    
    # Insert
    insert_database(barcode, size_category, hub_name, treatment, start_time)
    
    # Send to Arduino board2 (serial communication) 'HubInfo'
    write_serial_data(hub_name)
    
    
def main():
    # MQTT client thread start
    threading.Thread(target=mqtt_client_thread, daemon=True).start()

    # Serial thread start
    threading.Thread(target=serial_thread, daemon=True).start()
    
    motor_manager = MotorManager()

    try:
        while True:
            if motor_manager.start:
                write_serial_data('#S@START#')
            elif motor_manager.emg:
                print("sending to Arduino2 emergency signal ")
                write_serial_data('#S@EMGSTOP#')
            else:
                continue
            
    except KeyboardInterrupt:
        print("Program terminated")

if __name__ == "__main__":
    main()