import pymysql


def insert_database(full_number, category, hub_name, state):
    # setting
    con = pymysql.connect(host='localhost',
                          user='root',  
                          db='iot',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)


    try:
        with con.cursor() as cursor:
            # SQL query
            sql = "INSERT INTO products (full_number, category, hub_name, state) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (full_number, category, hub_name, state))
        
        # save
        con.commit()
        
        print("Complete insert database")
        
    finally:
        con.close()
