import pymysql

def connect(host_p, port_p, user_p, password_p, db_name_p = "ResourceDownloader"):
    db = pymysql.connect(host=host_p,
                         port=port_p,
                         user=user_p,
                         password=password_p)

    if db:
        print("Connect database success!")
    else:
        return None

    myCursor = db.cursor()
    myCursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name_p))

    return db