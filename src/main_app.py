from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication
from PyQt5 import uic
import sys
from ui_manager import UIManager
from motor_manager import MotorManager
from db_manager import DBManager

class WindowClass(QMainWindow, UIManager):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.ui_manager = UIManager()
        self.motor_manager = MotorManager()
        self.db_manager = DBManager()

    