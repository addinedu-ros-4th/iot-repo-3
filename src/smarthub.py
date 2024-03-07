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

cur.execute("select * from refueling")

columns = [column[0] for column in cur.description]
data = cur.fetchall()

df = pd.DataFrame(data, columns=columns)
df.reset_index(drop=True, inplace=True)
date_list = ["2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"]
categories = ["Li", "Fr", "Sh", "Ba"]
hubs = ["01", "02", "03", "NULL"]
states = ["0", "1", "2"]
df['checktime'] = np.random.choice(date_list, len(df))
df['checktime'] = pd.to_datetime(df['checktime'] + ' ' + np.random.choice(pd.date_range('00:00', '23:59', freq='min'), len(df)).astype(str))
df['category'] = np.random.choice(categories, len(df))
df['hub'] = np.random.choice(hubs, len(df))
df['state'] = np.random.choice(states, len(df))

# cur.execute("select min(checktime) from product")
# mindate = cur.fetchall()[0][0]
# cur.execute("select max(checktime) from product")
# maxdate = cur.fetchall()[0][0]
mindate = min(df['checktime'])
maxdate = max(df['checktime'])

print(df)
print(mindate, maxdate)

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pushSearch2.clicked.connect(self.searchproduct)
        # self.editStart.dateChanged.connect(self.mindatecheck)
        # self.editEnd.dateChanged.connect(self.maxdatecheck)

        self.cbDay.addItems(["All","2024-03-07", "2024-03-08", "2024-03-11", "2024-03-12", "2024-03-13"])
        self.cbDay.currentIndexChanged.connect(self.searchStat)
        # self.cbList.addItems(["-" ,"허브", "카테고리", "상태"])
        self.cbList.addItems(["-" ,"카테고리", "허브", "상태"])
        self.cbList.currentIndexChanged.connect(self.searchStat)

        self.serial_port = QSerialPort()
        self.serial_port.setPortName("B2")  # 아두이노의 포트명에 맞게 변경
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

    def searchproduct(self):
        start = self.editStart.date().toString("yyyy-MM-dd hh:mm:ss")
        end = self.editEnd.date().toString("yyyy-MM-dd hh:mm:ss")

        sql = "where checktime between '" + start + "' and '" + end + " ')"
        hub = self.cbHub.currentText()
        category = self.cbCategory.currentText()
        state = self.cbState.currentText()
        product_num = self.cbProductnum.currentText()

        pass

    # def mindatecheck(self):
    #     if self.editStart.date() < mindate:
    #         QMessageBox.warning(self, 'earlier than min', 'Set Minimum Birthday')
    #         self.editStart.setMinimumDate(mindate)

    # def maxdatecheck(self):
    #     if self.editEnd.date() > maxdate:
    #         QMessageBox.warning(self, 'later than max', 'Set Maximum Birthday')
    #         self.editEnd.setMaximumDate(maxdate)
    #     else:
    #         pass

    def searchStat(self):

        self.Day = self.cbDay.currentText()
        self.standard = self.cbList.currentText()
        if self.standard == "카테고리":
            self.standard = "category"
        elif self.standard == "허브":
            self.standard = "hub"
        elif self.standard == "상태":
            self.standard = "state"

        if self.Day == "All":
            self.df = df
        else:
            self.df = df[df['checktime'].dt.date == datetime.strptime(self.Day, "%Y-%m-%d").date()]
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
            sns.countplot(x=column, data=df, ax=ax, palette = "tab10") 
            
            self.canvas.draw_idle()

            pixmap = QPixmap(self.canvas.size())
            self.canvas.render(pixmap)
            pixmap = pixmap.scaled(self.Graphlabel.size(), aspectRatioMode=0)
            
            self.Graphlabel.setPixmap(pixmap)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())