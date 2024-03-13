
import mysql.connector
import pandas as pd

class DBManager:
    def __init__(self):
        self.remote = mysql.connector.connect(
            host="localhost",
            user="root",
            database="iot"
        )
        self.cur = self.remote.cursor(buffered=True)

        self.df = self.initialize_data()
        print("데이터베이스에 성공적으로 연결되었습니다.")
        print(self.remote)
        
        
    # products table 불러와서 dataframe화
    def initialize_data(self):
        self.cur.execute("select * from products")

        columns = [column[0] for column in self.cur.description]
        data = self.cur.fetchall()

        df = pd.DataFrame(data, columns=columns)
        df.reset_index(drop=True, inplace=True)
        return df
    
    
    def reconnect_cursor(self):
        self.remote = mysql.connector.connect(
            host="localhost",
            user="root",
            database="iot"
        )
        self.cur = self.remote.cursor(buffered=True)

        self.df = self.initialize_data()
        print("데이터베이스에 재연결하였습니다.")
        print(self.remote)
        
    
    def close_cursor(self):
        self.cur.close()