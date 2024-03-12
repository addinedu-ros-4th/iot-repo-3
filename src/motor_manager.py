from PyQt5.QtSerialPort import QSerialPort

class MotorManager :
    def __init__(self):
        pass
        # self.serial_port = QSerialPort()
        # self.serial_port.setPortName("/dev/ttyACM0")  # 아두이노의 포트명에 맞게 변경
        # self.serial_port.setBaudRate(QSerialPort.Baud9600)
        
    def moveconveyor(self):
        print("움직입니다")
        return True
        # self.serial_port.write(b'M')
        # self.serial_port.close()

    def stopconveyor(self):
        print("멈춰요")
        return True
        # self.serial_port.open(QSerialPort.WriteOnly)
        # self.serial_port.write(b'S')  
        # self.serial_port.close()
