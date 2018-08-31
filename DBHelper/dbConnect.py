import pymysql

def connect(host_p, port_p, user_p, password_p):
    db = pymysql.connect(host=host_p,
                         port=port_p,
                         user=user_p,
                         password=password_p)

    if db:
        print("Connect database success!")
        return db
    else:
        return None

def check_database(host, port, user, password, db, db_name_p = "ResourceDownloader"):
    myCursor = db.cursor()
    db_name = db_name_p
    ret = myCursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(db_name))
    if ret == 0:
        myCursor.execute("CREATE DATABASE {}".format(db_name))

    if db:
        db.close()
    
    new_db = pymysql.connect(host=host, port=port, user=user, password=password, database=db_name)
    if db:
        print("Re-connect to database success!")
        return new_db
    else:
        return None

def check_table(db, table_name="accounts_info"):
    myCursor = db.cursor()
    ret = myCursor.execute("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(table_name))
    print(ret)
