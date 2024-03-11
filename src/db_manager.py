import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import koreanize_matplotlib
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidgetItem

class DBManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.remote = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234",
            database="amrbase"
        )
        self.cur = self.remote.cursor(buffered=True)

        self.initialize_data()

    def initialize_data(self):
        self.cur.execute("select * from products")

        columns = [column[0] for column in self.cur.description]
        data = self.cur.fetchall()

        self.df = pd.DataFrame(data, columns=columns)
        self.df.reset_index(drop=True, inplace=True)

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

    # def searchproduct(self):
    #     start = self.ui_manager.editStart.dateTime().toString("yyyy-MM-dd hh:mm:ss")
    #     end = self.ui_manager.editEnd.dateTime().toString("yyyy-MM-dd hh:mm:ss")

    #     if self.ui_manager.cbChecktime.currentText() == "All":
    #         sql = "where ((start_time between '" + start + "' and '" + end + "') or (end_time between '" + start + "' and '" + end + "'))"
    #     elif self.ui_manager.cbChecktime.currentText() == "분류 시작":
    #         sql = "where (start_time between '" + start + "' and '" + end + "')"
    #     elif self.ui_manager.cbChecktime.currentText() == "분류 완료":
    #         sql = "where (end_time between '" + start + "' and '" + end + "')"

    #     size = self.ui_manager.cbSize.currentText()
    #     hub = self.ui_manager.cbHub.currentText()
    #     state = self.ui_manager.cbState.currentText()
    #     treatment = self.ui_manager.cbCategory.currentText()

    #     if size == 'All':
    #         size = ''
    #     elif size == '대':
    #         size = " and (size_category = 'LL')"
    #     elif size == '중':
    #         size = " and (size_category = 'MM')"
    #     elif size == '소':
    #         size = " and (size_category = 'SS')"
    #     else:
    #         size = " and (size_category not in ('LL', 'MM', 'SS'))"       

    #     if hub == 'All':
    #         hub = ''
    #     elif hub == '미분류':
    #         hub = " and (hub_name = '04')"
    #     else:
    #         hub = " and (hub_name = '" + self.ui_manager.cbHub.currentText() + "')"

    #     if state == 'All':
    #         state = ''
    #     elif state == '분류 중':
    #         state = " and (state = '00')"
    #     elif state == '분류 완료':
    #         state = " and (state = '01')"
    #     else:
    #         state = " and (state = '02')"
        
    #     if treatment == 'All':
    #         treatment = ''
    #     elif treatment == '액체':
    #         treatment = " and (treatment = 'LI')"
    #     elif treatment == '파손위험':
    #         treatment = " and (treatment = 'FR')"
    #     elif treatment == '부패성':
    #         treatment = " and (treatment = 'FR')"   
    #     else:
    #         treatment = " and (treatment = 'NO')"

    #     sql2 = sql + size + hub + state + treatment
    #     print(f"select size_category, hub_name, state, treatment, start_time, end_time from products {sql2}")
    #     self.cur.execute(f"select size_category, hub_name, state, treatment, start_time, end_time from products {sql2}")

    #     result = self.cur.fetchall()

    #     result = [list(t) for t in result]

    #     self.ui_manager.tableWidget.setRowCount(0)

    #     for a in result:
    #         row = self.ui_manager.tableWidget.rowCount()
    #         self.ui_manager.tableWidget.insertRow(row)
    #         for b in range(len(a)):
    #             # self.ui_manager.tableWidget.setItem(row, b, self.QTableWidgetItem(str(a[b])))
    #             item = QTableWidgetItem(str(a[b]))
    #             self.ui_manager.tableWidget.setItem(row, b, item)
