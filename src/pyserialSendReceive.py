import serial

inputs = []
isreturn = 0

ser = serial.Serial('/dev/ttyACM0', 9600, timeout =10)

while True:
    tmpstring = input("허브를 입력하세요: (예: 01) \n")
    
    if tmpstring != '': #serial write
        tmpsend = "#S@HUB,{}#".format(tmpstring)
        ser.write(bytes(tmpsend, "utf-8"))
        tmpstring = ''
    if ser.readable(): #serial read
        tmpmsg = ser.read(15)
        tmpdecode = tmpmsg.decode('utf-8')
        print(tmpdecode)
        
    else:
        print("none")
    
ser.close()