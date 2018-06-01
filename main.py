import json
import os
import platform
import traceback
from selenium import webdriver
import time

from module_utility.source_extract.cl_extract import extract_source_torrent
from module_utility.source_extract.cl_extract import analyze_link_torrent
from module_utility.source_extract.ph_extract import extract_ph_source

CONFIG_FILE = os.path.join("file_config", "config.json")
CL_1024_PATH = os.path.join("file_config", "cl_1024")
PH_PATH = os.path.join("file_config", "ph")

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


def getConfig(configData, configType):
    param_list = {}
    param_list["url"] = configData["cl1024"][0]["url"]
    param_list["id"] = configData["cl1024"][0]["id"]
    param_list["passwd"] = configData["cl1024"][0]["password"]
    param_list["data"] = os.path.join(CL_1024_PATH, configData["cl1024"][0][configType]["data_name"])
    param_list["bakData"] = os.path.join(CL_1024_PATH, configData["cl1024"][0][configType]["data_name_bak"])
    param_list["errorData"] = os.path.join(CL_1024_PATH, configData["cl1024"][0][configType]["error_data"])
    param_list["section"] = configData["cl1024"][0][configType]["section_code"]
    param_list["counting"] = configData["cl1024"][0][configType]["ranking_count"]
    return param_list

def main():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if  data["cl1024"][0]["url"] == "":
            print("Please input the address:")
            data["cl1024"][0]["url"] = input()
        if data["cl1024"][0]["id"] == "":
            print("Please input the id:")
            data["cl1024"][0]["id"] = input()
        if data["cl1024"][0]["password"] == "":
            print("Please input the password: ")
            data["cl1024"][0]["password"] = input()
        if data["ph"]["url"] == "":
            print("Please input the url: ")
            data["ph"]["url"] = input()
        if data["ph"]["view_keyid"] == "":
            print("Please input the keyID: ")
            data["ph"]["view_keyid"] = input()

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    section_map = ["nation", "NA_CODE_ASIA", "EURO", "CODE_ASIA", "comic", "ch_subs", "exchange"]
    MAX_SECTOR_SLEEP = 30 * 60

    try:
        phParamList = {"url":data["ph"]["url"], "viewKey":data["ph"]["view_keyid"],
                       "data_name":os.path.join(PH_PATH, data["ph"]["data_name"]),
                       "data_name_bak":os.path.join(PH_PATH, data["ph"]["data_back_name"]),
                       "data_name_error": os.path.join(PH_PATH, data["ph"]["data_error_name"])}

        if platform.system() == "Windows":
            driver = webdriver.Chrome("D:\Chrome_Download\chromedriver_win32\chromedriver.exe")
        else:
            driver = ""
        extract_ph_source(driver, phParamList)
        
        for sec_id in section_map:
            param_list = getConfig(data, sec_id)
            print(param_list)
            driver = cl_login(param_list)
            extract_source_torrent(driver, param_list)
            driver.close()
            time.sleep(MAX_SECTOR_SLEEP)

        for sec_id in section_map:
            param_list = getConfig(data, sec_id)
            print(param_list)
            if platform.system() == "Linux":
                driver = ""
            else:
                driver = cl_login(param_list)
            analyze_link_torrent(driver, param_list)

        '''
        #Get nation section
        param_list = getConfig(data, "nation")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        if platform.system() == "Linux":
            driver.close()
        analyze_link_torrent(driver, param_list)
        if platform.system() == "Windows":
            driver.close()
        time.sleep(100)


        #Get NA_asia section
        param_list = getConfig(data, "NA_CODE_ASIA")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)

        #Get EURO section
        param_list = getConfig(data, "EURO")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)

        #Get CODE_ASIA section
        param_list = getConfig(data, "CODE_ASIA")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)

        #Get comic section
        param_list = getConfig(data, "comic")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)

        #Get ch_subs section
        param_list = getConfig(data, "ch_subs")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)

        #Get exchange section
        param_list = getConfig(data, "exchange")
        print(param_list)
        driver = cl_login()
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
        driver.close()
        time.sleep(100)
        '''

    except Exception as e:
        print("")
        print("str(Exception):\t", str(Exception))
        print("str(e):\t\t", str(e))
        print("repr(e):\t", repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    driver.close()


main()
