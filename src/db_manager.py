
import mysql.connector
import pandas as pd

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

        self.df = self.initialize_data()
        


    # products table 불러와서 dataframe화
    def initialize_data(self):
        self.cur.execute("select * from products")

        columns = [column[0] for column in self.cur.description]
        data = self.cur.fetchall()

        df = pd.DataFrame(data, columns=columns)
        df.reset_index(drop=True, inplace=True)
        return df