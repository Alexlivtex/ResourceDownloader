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

def check_database(db, db_name_p = "ResourceDownloader"):
    myCursor = db.cursor()
    ret = myCursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(db_name_p))
    if ret == 0:
        myCursor.execute("CREATE DATABASE {}".format(db_name_p))
    else:
        print("Data base {} has already exists!".format(db_name_p))
    return db

def check_table(db, table_name="accounts_info"):
    myCursor = db.cursor()
    ret = myCursor.execute("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(table_name))
    print(ret)