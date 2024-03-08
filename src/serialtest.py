import serial
import time
import sys
import tty
import termios

def getch():
    """단일 문자를 받아옴"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


timer = 0
cnt =1
inputs = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout =10)

print("입력을 받고자 하는 내용을 입력한 후 Enter를 누르세요.")
# print("종료하려면 'esc' 키를 누르세요.")

while True:
    char = getch()

    if char == '\r':
        input_text = ''.join(inputs)
        print("사용자 입력:", input_text)
        tmpstr = "#S@HUB,{}#".format(input_text)
        ser.write(bytes(tmpstr, "utf-8"))
        inputs = []  # 변수 초기화
    elif char == '\x1b':  # ESC 키 누르면 종료
        print("프로그램을 종료합니다.")
        break
    else:
        inputs.append(char)

# while(1):
#     if timer == 10:
#         if cnt <= 3 :
#             tmpstr = "#S@HUB,{:02d}#".format(cnt)
#             ser.write(bytes(tmpstr, "utf-8"))
#             print(tmpstr)
#             cnt +=1
#         else:
#             cnt = 1

#         timer =0
        
#     else:
#         timer+=1
#         print(timer)
    
#     time.sleep(1)


ser.close()