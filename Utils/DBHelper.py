import pymysql

def connect(host_p, port_p, user_p, password_p):
    db = pymysql.connect(host=host_p,
                         port=port_p,
                         user=user_p,
                         password=password_p)

    if db:
        return db
    else:
        return None


def check_database(host, port, user, password, db, db_name_p):
    myCursor = db.cursor()
    db_name = db_name_p
    SQL_CHECK = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(db_name)
    ret = myCursor.execute(SQL_CHECK)
    if ret == 0:
        myCursor.execute("CREATE DATABASE {}".format(db_name))

    if db:
        db.close()

    new_db = pymysql.connect(host=host, port=port, user=user, password=password, database=db_name, charset="utf8")
    if db:
        return new_db
    else:
        return None

def check_table(db, table_name):
    myCursor = db.cursor()
    SQL_CHECK = "SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(table_name)
    ret = myCursor.execute(SQL_CHECK)
    return ret

def create_table(db, createSQL):
    try:
        myCursor = db.cursor()
        print(createSQL)
        myCursor.execute(createSQL)
        myCursor.close()
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

def insert_table(db, insertSQL, insertData=None):
    try:
        myCursor = db.cursor()
        print(insertSQL)
        if not insertData:
            myCursor.execute(insertSQL)
        else:
            myCursor.execute(insertSQL, insertData)
        myCursor.close()
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

def fetchData(db, fetchSQL):
    myCursor = db.cursor()
    myCursor.execute(fetchSQL)
    return myCursor