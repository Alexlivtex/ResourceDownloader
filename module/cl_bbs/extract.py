import pymysql
import time

def extract_cl_bbs_data(db, driver):
    AccountTable = "Accounts_info"
    myCursor = db.cursor()
    ret = myCursor.execute("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(AccountTable))
    print(ret)
    if ret == 0:
        try:
            myCursor.execute("CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ,"
                             "Module VARCHAR (100) not NULL , "
                             "Address VARCHAR (100) NOT NULL , "
                             "UserName VARCHAR (100) NOT NULL ,"
                             "Password VARCHAR(100) NOT  NULL )".format(AccountTable))

            module = "cl_bbs"
            address = input("Please input the cl_bbs address : ")
            user_name = input("Please input the username : ")
            password = input("Please input the password : ")

            InsertSQL = "INSERT INTO {} (Module, Address, UserName, Password) VALUES ('{}', '{}', '{}', '{}' )".format(AccountTable, str(module), str(address), str(user_name), str(password))
            print(InsertSQL)
            myCursor.execute(InsertSQL)

            myCursor.close()
            db.commit()
        except Exception as err:
            db.rollback()
            raise err

    myCursor.execute("SELECT * FROM {}".format(AccountTable))
    record = myCursor.fetchone()

    address = record[2]
    user_name = record[3]
    password = record[4]

    login_url = address + "/login.php"

    print(login_url)

    driver.set_page_load_timeout(50)
    driver.set_script_timeout(50)
    driver.get(login_url)

    time.sleep(100)

    elem_user_name = driver.find_element_by_name("pwuser")
    elem_user_pasword = driver.find_element_by_name("pwpwd")
    elem_user_name.send_keys(user_name)
    elem_user_pasword.send_keys(password)
    elem_login = driver.find_element_by_name("submit")
    time.sleep(3)
    elem_login.click()
    time.sleep(2)