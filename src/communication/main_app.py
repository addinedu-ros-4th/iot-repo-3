from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer, Qt
from ui_manager import UIManager
from motor_manager import MotorManager
from db_manager import DBManager
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import seaborn as sns
import koreanize_matplotlib
# import resources_rc
# 터미널에서 pyrcc5 -o resources_rc.py <resources.qrc경로> 실행 요구

from_class = uic.loadUiType("smarthub.ui")[0]

class WindowClass(QMainWindow, UIManager):
    def __init__(self):
        super().__init__()
        # self.setup_ui()
        self.ui_manager = UIManager()
        self.motor_manager = MotorManager()
        self.db_manager = DBManager()

        self.test = self.db_manager.df.copy()

        self.pushStart.clicked.connect(self.moveconveyor)
        self.pushStart2.clicked.connect(self.moveconveyor)
        self.pushStart3.clicked.connect(self.moveconveyor)
        self.pushStop.clicked.connect(self.stopconveyor)
        self.pushStop2.clicked.connect(self.stopconveyor)
        self.pushStop3.clicked.connect(self.stopconveyor)

        self.pushSearch2.clicked.connect(self.searchproduct)
        self.pushReset.clicked.connect(self.resettable)
        self.cbDay.currentIndexChanged.connect(self.searchStat)
        self.cbList.currentIndexChanged.connect(self.searchStat)

        # 1초 단위 주기로 timeout signal 발생시켜서 displaybarcode 실행
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.displaybarcode)
        self.timer.start(500)

    # 모터의 상태(가동중/대기중)에 따라 겹쳐있는 라벨 toggle하여 show    
    def setConveyorLabels(self, is_running):
        on_labels = [self.labelOn, self.labelOn2, self.labelOn3]
        off_labels = [self.labelOff, self.labelOff2, self.labelOff3]

        for label in on_labels:
            label.setVisible(is_running)

        for label in off_labels:
            label.setVisible(not is_running)

    def setStartStopLabels(self, is_running):
        move_labels = [self.pushStart, self.pushStart2, self.pushStart3]
        stop_labels = [self.pushStop, self.pushStop2, self.pushStop3]

        for label in move_labels:
            label.setVisible(is_running)

        for label in stop_labels:
            label.setVisible(not is_running)

    # 긴급 정지했던 모터 재가동
    def moveconveyor(self):
        self.setConveyorLabels(True)
        self.setStartStopLabels(False)
        self.motor_manager.moveconveyor()

    # 모터 긴급 정지
    def stopconveyor(self):
        self.setConveyorLabels(False)
        self.setStartStopLabels(True)
        self.motor_manager.stopconveyor()

    # 현재 모터 동작여부 확인해서 UI상에 가동중/대기중 표시
    # def check_motor(self):
    #     self.motor_manager.check_motor()

    def displaybarcode(self):
        self.db_manager.reconnect_cursor()
        sql3 = "select barcode, state, hub_name from products"
        self.db_manager.cur.execute(f"{sql3}")

        barstahub = self.db_manager.cur.fetchall()
        barstahub = [list(u) for u in barstahub]

        df2 = pd.DataFrame(barstahub, columns=['barcode', 'state', 'hub_name'])

        condition = df2['state']=='00'

        if any(condition):
            movingbarcode = df2.loc[condition, 'barcode'].values[-1]
            movinghub = df2.loc[condition, 'hub_name'].values[-1]

            # barcode가 string이 아닐 경우
            movingbarcode = str(movingbarcode)

            self.label_6.setText(movingbarcode)

            if movinghub == '01':
                self.labelhub11.setText("분류 중")
                self.labelhub22.setText("")
                self.labelhub33.setText("")
                self.labelhub1.setStyleSheet("background-color:green; color:white; border-style:solid; border-radius:30px; border-width:3px; border-color:green;")
                self.labelhub2.setStyleSheet("border-radius : 30px; background-color : white;")
                self.labelhub3.setStyleSheet("border-radius : 30px; background-color : white;")
            elif movinghub == '02':
                self.labelhub33.setText("")
                self.labelhub22.setText("분류 중")
                self.labelhub11.setText("")
                self.labelhub1.setStyleSheet("border-radius : 30px; background-color : white;")
                self.labelhub2.setStyleSheet("background-color:green; color:white; border-style:solid; border-radius:30px; border-width:3px; border-color:green;")
                self.labelhub3.setStyleSheet("border-radius : 30px; background-color : white;")
            else:
                self.labelhub11.setText("")
                self.labelhub22.setText("")
                self.labelhub33.setText("분류 중")
                self.labelhub1.setStyleSheet("border-radius : 30px; background-color : white;")
                self.labelhub2.setStyleSheet("border-radius : 30px; background-color : white;")
                self.labelhub3.setStyleSheet("background-color:green; color:white; border-style:solid; border-radius:30px; border-width:3px; border-color:green;")
        else:
            self.labelhub1.setStyleSheet("border-radius : 30px; background-color : white;")
            self.labelhub2.setStyleSheet("border-radius : 30px; background-color : white;")
            self.labelhub3.setStyleSheet("border-radius : 30px; background-color : white;")
            self.label_6.setText('') 
            self.labelhub11.setText('')
            self.labelhub22.setText('')
            self.labelhub33.setText('')


        self.db_manager.close_cursor()


    # 쿼리를 이용해서 날짜 범위, 콤보박스 선택에 따라 QTableWidget에 데이터 출력
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
        self.db_manager.cur.execute(f"select size_category, hub_name, state, treatment, start_time, end_time from products {sql2}")

        result = self.db_manager.cur.fetchall()

        result = [list(t) for t in result]

        self.tableWidget.setRowCount(0)
        for a in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for b in range(len(a)):
                self.tableWidget.setItem(row, b, QTableWidgetItem(str(a[b])))

    # 물품찾기 데이터 테이블 내용 지우기
    def resettable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    # 주문 통계 데이터 처리일, 통계 기준 설정
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
            self.test = self.db_manager.df.copy()
        else:
            self.test = self.db_manager.df[self.db_manager.df['end_time'].dt.date == datetime.strptime(self.Day, "%Y-%m-%d").date()].copy()
        
        self.plot_graph(self.test, self.standard)

    # pixmap에 그래프 그려주기
    def plot_graph(self, df, column):
    
        self.figure = Figure(figsize=(6, 4))
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
    my_windows = WindowClass()
    my_windows.show()
    sys.exit(app.exec_())