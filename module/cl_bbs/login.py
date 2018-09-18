from Utils import webOperation
from Utils import DBHelper
import time

def login_website(db):
    AccountTable = "Accounts_info"
    webhandle = webOperation.openBrowser()

    FETCH_SQL = "SELECT * FROM {}".format(AccountTable)
    cursor = DBHelper.fetchData(db, FETCH_SQL)
    record = cursor.fetchone()

    address = record[2]
    user_name = record[3]
    password = record[4]

    login_url = address + "/login.php"

    print(login_url)

    webhandle.set_page_load_timeout(50)
    webhandle.set_script_timeout(50)
    webhandle.get(login_url)

    elem_user_name = webhandle.find_element_by_name("pwuser")
    elem_user_pasword = webhandle.find_element_by_name("pwpwd")
    elem_user_name.send_keys(user_name)
    elem_user_pasword.send_keys(password)
    elem_login = webhandle.find_element_by_name("submit")
    time.sleep(3)
    elem_login.click()
    time.sleep(10)
    return webhandle
