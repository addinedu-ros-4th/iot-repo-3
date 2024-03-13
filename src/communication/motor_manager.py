class MotorManager :
    def __init__(self):
        self.emg = False
        self.start = False
        
    def moveconveyor(self):
        print("Restart")
        self.start = True

    def stopconveyor(self):
        print("Emegency !")
        self.emg = True
        