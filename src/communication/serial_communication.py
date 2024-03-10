import serial
import time


def write_serial_data(hub_name):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)
    
    if ser.isOpen():
        print("Serial port is open!")
        tmpsend = "#S@HUB,{}#".format(hub_name) # 데이터 형식 : #보드명@데이터, {허브명}#
        ser.write(bytes(tmpsend, "utf-8"))      # 데이터 전송

        time.sleep(0.5)
        
        while ser.in_waiting > 0:  # 대기 중인 데이터가 있는지 확인
            tmpmsg = ser.read(ser.in_waiting)
            tmpdecode = tmpmsg.decode('utf-8')
            print(tmpdecode)

        ser.close()
        
    else:
        print("Serial port is not open!")


def get_serial_data(hub_name):
    pass