import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtSerialPort import QSerialPort
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import koreanize_matplotlib


from_class = uic.loadUiType("smarthub.ui")[0]

remote = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "1234",
    database = "amrbase"
)
cur = remote.cursor(buffered=True)

cur.execute("select * from products") # refueling -> products table로 수정

columns = [column[0] for column in cur.description]
data = cur.fetchall()

df = pd.DataFrame(data, columns=columns)
df.reset_index(drop=True, inplace=True)

# 칼럼 임의 생성(추후 데이터베이스 이용할 때 삭제)
# date_list = ["2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"]
# size_list = ["LL", "MM", "SS", "XX"]
# categories = ["LI", "FR", "SH", "NO"]
# hubs = ["01", "02", "03"]
# states = ["00", "01"]
# df['end_time'] = np.random.choice(date_list, len(df))
# df['end_time'] = pd.to_datetime(df['end_time'] + ' ' + np.random.choice(pd.date_range('00:00', '23:59', freq='min'), len(df)).astype(str))
# df['start_time'] = df['end_time'] - pd.to_timedelta(np.random.randint(1, 1440, len(df)), unit='min')
# df['size_category'] = np.random.choice(size_list, len(df))
# df['hub_name'] = np.random.choice(hubs, len(df))
# df['state'] = np.random.choice(states, len(df))
# df['treatment'] = np.random.choice(categories, len(df))
# df.loc[df['size_category'] == "XX", ['state', 'hub_name']] = ["02", "04"]
# df.loc[df['size_category'] == "XX", 'size_category'] = [''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 2)) for _ in range((df['size_category'] == "XX").sum())]
# print(df[["start_time", "end_time"]])

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.cbChecktime.addItems(["All", "분류 시작", "분류 완료"])
        self.cbSize.addItems(["All", "대", "중", "소", "알 수 없음"])
        self.cbHub.addItems(["All", "01", "02", "03", "미분류"])
        self.cbState.addItems(["All", "분류 중", "분류 완료", "분류 실패"])
        self.cbCategory.addItems(["All", "액체", "파손위험", "부패성", "그 외"])
        self.pushSearch2.clicked.connect(self.searchproduct)
        self.pushReset.clicked.connect(self.resettable)

        self.cbDay.addItems(["All","2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"])
        self.cbDay.currentIndexChanged.connect(self.searchStat)
        self.cbList.addItems(["-" ,"크기", "허브", "상태", "취급"])
        self.cbList.currentIndexChanged.connect(self.searchStat)

        self.serial_port = QSerialPort()
        self.serial_port.setPortName("/dev/ttyACM0")  # 아두이노의 포트명에 맞게 변경
        self.serial_port.setBaudRate(QSerialPort.Baud9600)

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

    def moveconveyor(self):

        self.labelOn.show()
        self.labelOn2.show()
        self.labelOn3.show()
        self.labelOff.hide()
        self.labelOff2.hide()
        self.labelOff3.hide()

        print("conveyor moving")
        self.serial_port.open(QSerialPort.WriteOnly)
        self.serial_port.write(b'R')
        self.serial_port.close()

        pass

    def stopconveyor(self):

        self.labelOn.hide()
        self.labelOn2.hide()
        self.labelOn3.hide()
        self.labelOff.show()
        self.labelOff2.show()
        self.labelOff3.show()

        print("conveyor stopped")
        self.serial_port.open(QSerialPort.WriteOnly)
        self.serial_port.write(b'S')  
        self.serial_port.close()

        pass

    def check_motor(self):
        self.serial_port.open(QSerialPort.WriteOnly)
        self.serial_port.write(b'F')
        self.serial_port.close()

    def searchproduct(self):
        start = self.editStart.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        end = self.editEnd.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        if self.cbChecktime.currentText() == "All":
            sql = "where ((start_time between '" + start + "' and '" + end + "') or (end_time between '" + start + "' and '" + end + "'))"
        elif self.cbChecktime.currentText() == "분류 시작":
            sql = "where (start_time between '" + start + "' and '" + end + "')"
        elif self.cbChecktime.currentText() == "분류 완료":
            sql = "where (end_time between '" + start + "' and '" + end + "')"

        size = self.cbSize.currentText()
        hub = self.cbHub.currentText()
        state = self.cbState.currentText()
        treatment = self.cbCategory.currentText()

        if size == 'All':
            size = ''
        elif size == '대':
            size = " and (size_category = 'LL')"
        elif size == '중':
            size = " and (size_category = 'MM')"
        elif size == '소':
            size = " and (size_category = 'SS')"
        else:
            size = " and (size_category not in ('LL', 'MM', 'SS'))"       

        if hub == 'All':
            hub = ''
        elif hub == '미분류':
            hub = " and (hub_name = '04')"
        else:
            hub = " and (hub_name = '" + self.cbHub.currentText() + "')"

        if state == 'All':
            state = ''
        elif state == '분류 중':
            state = " and (state = '00')"
        elif state == '분류 완료':
            state = " and (state = '01')"
        else:
            state = " and (state = '02')"
        
        if treatment == 'All':
            treatment = ''
        elif treatment == '액체':
            treatment = " and (treatment = 'LI')"
        elif treatment == '파손위험':
            treatment = " and (treatment = 'FR')"
        elif treatment == '부패성':
            treatment = " and (treatment = 'FR')"   
        else:
            treatment = " and (treatment = 'NO')"

        sql2 = sql + size + hub + state + treatment
        print(f"select size_category, hub_name, state, treatment, start_time, end_time from products {sql2}")
        cur.execute(f"select size_category, hub_name, state, treatment, start_time, end_time from products {sql2}")

        result = cur.fetchall()

        result = [list(t) for t in result]

        self.tableWidget.setRowCount(0)
        for a in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for b in range(len(a)):
                self.tableWidget.setItem(row, b, QTableWidgetItem(str(a[b])))

    def resettable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def searchStat(self):

        self.Day = self.cbDay.currentText()
        self.standard = self.cbList.currentText()
        if self.standard == "크기":
            self.standard = "size_category"
        elif self.standard == "허브":
            self.standard = "hub_name"
        elif self.standard == "상태":
            self.standard = "state"
        elif self.standard == "취급":
            self.standard = "treatment"

        if self.Day == "All":
            self.df = df
        else:
            self.df = df[df['end_time'].dt.date == datetime.strptime(self.Day, "%Y-%m-%d").date()]
            print("debuging~~")
        self.plot_graph(self.df, self.standard)


    def plot_graph(self, df, column):
    
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.pixmap = QPixmap()
        self.Graphlabel.setPixmap(self.pixmap)
        
        if self.standard == "-":
            pass
        else:
            ax = self.figure.add_subplot(111)
            sns.countplot(x=column, data=df, ax=ax, palette = "YlGnBu") 
            
            self.canvas.draw_idle()

            self.pixmap = QPixmap(self.canvas.size())
            self.canvas.render(self.pixmap)
            self.pixmap = self.pixmap.scaled(self.Graphlabel.size(), aspectRatioMode=0)
            
            self.Graphlabel.setPixmap(self.pixmap)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())