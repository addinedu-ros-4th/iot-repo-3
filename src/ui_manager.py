from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys

class UIManager(QDialog) :
    def __init__(self):
        super().__init__()
        uic.loadUi("smarthub.ui", self)
        self.setup_ui()

    def setup_ui(self):
        
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.cbChecktime.addItems(["All", "분류 시작", "분류 완료"])
        self.cbSize.addItems(["All", "대", "중", "소", "알 수 없음"])
        self.cbHub.addItems(["All", "01", "02", "03", "미분류"])
        self.cbState.addItems(["All", "분류 중", "분류 완료", "분류 실패"])
        self.cbCategory.addItems(["All", "액체", "파손위험", "부패성", "그 외"])
        
        self.cbDay.addItems(["All","2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"])
        self.cbList.addItems(["-" ,"크기", "허브", "상태", "취급"])
        
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

        self.pushMain.clicked.connect(self.mainmode)
        self.pushMain2.clicked.connect(self.mainmode)

    def mainmode(self):

        self.group1.show()
        self.group2.hide()
        self.group3.hide()

    def productsearchmode(self):

        self.group1.hide()
        self.group2.show()
        self.group3.hide()

    def statisticsmode(self):

        self.group1.hide()
        self.group2.hide()
        self.group3.show()

    def productsearch(self):

        self.productsearchmode()

    def orderstatistics(self):

        self.statisticsmode()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_manager = UIManager()
    ui_manager.show()
    sys.exit(app.exec_())