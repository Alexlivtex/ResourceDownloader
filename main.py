import json
import os
import platform
import traceback
from selenium import webdriver

from module_utility.source_extract.cl_extract import extract_source_torrent
from module_utility.source_extract.cl_extract import analyze_link_torrent

CONFIG_FILE = os.path.join("file_config", "config.json")
CL_1024_PATH = os.path.join("file_config", "cl_1024")

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

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    if platform.system() == "Windows":
        driver = webdriver.Chrome("D:\Chrome_Download\chromedriver_win32\chromedriver.exe")
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=options)

    try:
        param_list = getConfig(data, "nation")
        print(param_list)
        extract_source_torrent(driver, param_list)
        analyze_link_torrent(driver, param_list)
    except Exception as e:
        print("")
        print("str(Exception):\t", str(Exception))
        print("str(e):\t\t", str(e))
        print("repr(e):\t", repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    driver.close()


main()
