import platform
import time
from selenium import webdriver


def cl_login(paramList):
    if platform.system() == "Windows":
        driver = webdriver.Chrome("D:\Chrome_Download\chromedriver_win32\chromedriver.exe")
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=options)

    id = paramList["id"]
    url = paramList["url"]
    passwd = paramList["passwd"]

    login_url = url + "/login.php"

    driver.set_page_load_timeout(50)
    driver.set_script_timeout(50)
    driver.get(login_url)

    elem_user_name = driver.find_element_by_name("pwuser")
    elem_user_pasword = driver.find_element_by_name("pwpwd")
    elem_user_name.send_keys(id)
    elem_user_pasword.send_keys(passwd)
    elem_login = driver.find_element_by_name("submit")
    time.sleep(3)
    elem_login.click()
    time.sleep(2)

    return driver
