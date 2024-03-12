import pymysql
from datetime import datetime

def get_db_connection():
    # setting
    conn = pymysql.connect(host='localhost',
                          user='root',  
                          db='iot',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

    return conn


def close_db_connection(conn):
    # close connect
    conn.close()


def insert_database(barcode, size_category, hub_name, treatment, start_time):
    
    # setting
    conn = get_db_connection()
    

    try:
        with conn.cursor() as cursor:
            # SQL Query
            sql = "INSERT INTO products (barcode, size_category, hub_name, treatment, start_time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (barcode, size_category, hub_name, treatment, start_time))


            if hub_name == '04':
                state = '02' #분류 불가
                update_sql = "UPDATE products SET state = %s WHERE hub_name = %s"
                cursor.execute(update_sql, (state, hub_name))
                
        # save
        conn.commit()
            
        print("Complete insert database")
        

    except pymysql.err.IntegrityError as e:     # primary key는 1개만 들어올 수 있다.
        print(f"already recognized !")
        
    finally:
        close_db_connection(conn)


# Find columns
def change_state(barcode):
    # setting
    conn = get_db_connection()
    
    sql = "SELECT state, end_time FROM products WHERE barcode = %s"
    cur = conn.cursor()
    cur.execute(sql, (barcode, ))
    
    results = cur.fetchall()
    
    if results:
        # 첫 번째 결과 행만 사용
        state, end_time = results[0] # data unpacking
    else:
        print("해당 바코드에 대한 결과가 없습니다.")


    # Data update
    if state is not None:
        state = '01'
        end_time = datetime.now()
                
        update_database(cur, barcode, state, end_time)
                
        conn.commit()
        close_db_connection(conn)
                
        print(f"{barcode} 분류 완료.")
        
        return '#S@STATEUPDATE'


def update_database(cur, barcode, state, end_time):
    sql = "UPDATE products SET state = %s, end_time = %s\
        WHERE barcode = %s";
        
    cur.execute(sql, (state, end_time, barcode))
    
