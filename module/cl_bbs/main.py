import time
from Utils import DBHelper

from .extract_source import extract_source_torrent

def extract_cl_bbs_data(db, driver):
    AccountTable = "Accounts_info"
    ret = DBHelper.check_table(db, AccountTable)
    print(ret)
    if ret == None:
        CREATE_SQL = "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ," \
                     "Module VARCHAR (100) not NULL ," \
                     "Address VARCHAR (100) NOT NULL , " \
                     "UserName VARCHAR (100) NOT NULL ," \
                     "Password VARCHAR(100) NOT  NULL )".format(AccountTable)
        DBHelper.create_table(db, CREATE_SQL)

        module = "cl_bbs"
        address = input("Please input the cl_bbs address : ")
        user_name = input("Please input the username : ")
        password = input("Please input the password : ")

        INSERT_SQL = InsertSQL = "INSERT INTO {} (Module, Address, UserName, Password) VALUES ('{}', '{}', '{}', '{}' )".format(AccountTable, str(module), str(address), str(user_name), str(password))
        DBHelper.insert_table(db, INSERT_SQL)


    FETCH_SQL = "SELECT * FROM {}".format(AccountTable)
    cursor = DBHelper.fetchData(db, FETCH_SQL)
    record = cursor.fetchone()

    address = record[2]
    user_name = record[3]
    password = record[4]

    login_url = address + "/login.php"

    print(login_url)

    driver.set_page_load_timeout(50)
    driver.set_script_timeout(50)
    driver.get(login_url)

    time.sleep(2)

    elem_user_name = driver.find_element_by_name("pwuser")
    elem_user_pasword = driver.find_element_by_name("pwpwd")
    elem_user_name.send_keys(user_name)
    elem_user_pasword.send_keys(password)
    elem_login = driver.find_element_by_name("submit")
    time.sleep(3)
    elem_login.click()
    time.sleep(10)

    myCursor = db.cursor()
    cl_video_db = "bbs_video_Data"

    ret = DBHelper.check_table(db, cl_video_db)
    if ret == 0:
        print("Data base not exists!")

        CREATE_SQL = "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ," \
                     "Title VARCHAR (500) not NULL ," \
                     "Link VARCHAR (128) NOT NULL ," \
                     "Section INT  NOT NULL ," \
                     "TorrentLink VARCHAR(100) NOT  NULL ," \
                     "DownloadingCount INT NOT  NULL )".format(cl_video_db)

        '''
        CREATE_SQL = "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ," \
                     "Title VARCHAR (500) not NULL ," \
                     "Link VARCHAR (128) NOT NULL ," \
                     "TorrentLink VARCHAR(100) NOT  NULL)".format(cl_video_db)
        '''

        DBHelper.create_table(db, CREATE_SQL)
    else:
        print("cl_bbs data already exists!")

    video_section = [2, 15, 4, 5, 25, 26, 27]
    for video_section_id in video_section:
        extract_source_torrent(driver, address, db, cl_video_db, video_section_id)
