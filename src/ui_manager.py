import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtSerialPort import QSerialPort
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class UIManager(QMainWindow) :
    def __init__(self):
        super().__init__()
        uic.loadUi("smarthub.ui", self)
        self.setup_ui()

    def setup_ui(self):
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pushSearch2.clicked.connect(self.searchproduct)

        self.cbDay.addItems(["All","2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"])
        self.cbDay.currentIndexChanged.connect(self.searchStat)
        # self.cbList.addItems(["-" ,"허브", "카테고리", "상태"])
        self.cbList.addItems(["-" ,"카테고리", "허브", "상태"])
        self.cbList.currentIndexChanged.connect(self.searchStat)

        self.labelOn.hide()
        self.labelOn2.hide()
        self.labelOn3.hide()
        self.labelOff.hide()
        self.labelOff2.hide()
        self.labelOff3.hide()
        self.group1.show()
        self.group2.hide()
        self.group3.hide()

        self.pushSearch.clicked.connect(self.productsearch)
        self.pushStat.clicked.connect(self.orderstatistics)
        
        self.pushStart.clicked.connect(self.moveconveyor)
        self.pushStart2.clicked.connect(self.moveconveyor)
        self.pushStart3.clicked.connect(self.moveconveyor)
        self.pushStop.clicked.connect(self.stopconveyor)
        self.pushStop2.clicked.connect(self.stopconveyor)
        self.pushStop3.clicked.connect(self.stopconveyor)

        self.pushMain.clicked.connect(self.mainmode)
        self.pushMain2.clicked.connect(self.mainmode)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_manager = UIManager()
    ui_manager.show()
    sys.exit(app.exec_())