from PyQt5.QtSerialPort import QSerialPort

class MotorManager :
    def __init__(self):
        self.serial_port = QSerialPort()
        self.serial_port.setPortName("B2")  # 아두이노의 포트명에 맞게 변경
        self.serial_port.setBaudRate(QSerialPort.Baud9600)

    def moveconveyor(self):

        self.labelOn.show()
        self.labelOn2.show()
        self.labelOn3.show()
        self.labelOff.hide()
        self.labelOff2.hide()
        self.labelOff3.hide()

        self.serial_port.open(QSerialPort.WriteOnly)
        self.serial_port.write(b'S')
        self.serial_port.close()

        pass

    def stopconveyor(self):

        self.labelOn.hide()
        self.labelOn2.hide()
        self.labelOn3.hide()
        self.labelOff.show()
        self.labelOff2.show()
        self.labelOff3.show()

        self.serial_port.open(QSerialPort.WriteOnly)
        self.serial_port.write(b'T')  
        self.serial_port.close()

        pass