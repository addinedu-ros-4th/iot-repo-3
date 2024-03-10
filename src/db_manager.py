import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import koreanize_matplotlib

class DBManager:
    def __init__(self):
        self.remote = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234",
            database="amrbase"
        )

        self.cur = self.remote.cursor(buffered=True)

        self.cur.execute("select * from refueling")

        columns = [column[0] for column in self.cur.description]
        data = self.cur.fetchall()

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

    def searchproduct(self):
        start = self.editStart.date().toString("yyyy-MM-dd hh:mm:ss")
        end = self.editEnd.date().toString("yyyy-MM-dd hh:mm:ss")

        sql = "where checktime between '" + start + "' and '" + end + " ')"
        hub = self.cbHub.currentText()
        category = self.cbCategory.currentText()
        state = self.cbState.currentText()
        product_num = self.cbProductnum.currentText()

        pass

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
