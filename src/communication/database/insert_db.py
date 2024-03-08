import pymysql


def insert_database(barcode, size_category, hub_name, treatment, start_time):
    # setting
    con = pymysql.connect(host='localhost',
                          user='root',  
                          db='iot',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)


    try:
        with con.cursor() as cursor:
            # SQL Query
            sql = "INSERT INTO products (barcode, size_category, hub_name, treatment, start_time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (barcode, size_category, hub_name, treatment, start_time))



            if hub_name == '04':
                state = '02' #분류 불가
                update_sql = "UPDATE products SET state = %s WHERE hub_name = %s"
                cursor.execute(update_sql, (state, hub_name))
        
                
        # save
        con.commit()
        
        print("Complete insert database")

    except pymysql.err.IntegrityError as e:     # primary key는 1개만 들어올 수 있다.
        print(f"already recognized !")
        
    finally:
        con.close()
