import serial
inputs = []
isreturn = 0
import time
    
    
def connect():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)
        print("Serial port connected successfully.")
        return ser
    except Exception as e:
        print(f"Failed to connect to serial port: {e}")
        return None
    
    
def disconnect(ser):
    ser.close()


def write_serial_data(ser, hub_name):
    if ser.isOpen():
        print("Serial port is open!")
        print(f"Sending hub_name: {hub_name}")
            
        if hub_name: # hub_name 값이 있는 경우에만 데이터 전송
            data_to_send = hub_name #"#S@HUB,{}#".format(hub_name)
            print(data_to_send)
            
            ser.write(bytes(data_to_send, "utf-8"))
            time.sleep(3)  # 아두이노가 데이터를 처리할 시간
            print("Data sent successfully.")
                
            # if ser.in_waiting: # 수신된 데이터가 있는지 확인
            #     response = ser.read(ser.in_waiting).decode('utf-8')
            #     print(f"Received response: {response}")
            # else:
            #     print("No response received.")    
    else:
        print("Serial port is not open.")


def get_serial_data(data):
    pass