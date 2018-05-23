import json
import os
import platform
from selenium import webdriver

from module_utility.source_extract.cl_extract import extract_source_asis_nocode
from module_utility.source_extract.cl_extract import analyze_link
from module_utility.source_extract.cl_extract import ranking

CONFIG_FILE = os.path.join("file_config", "config.json")
CL_1024_PATH = os.path.join("file_config", "cl_1024")


def main():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        url = data["cl1024"][0]["url"]
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
        #extract_source_asis_nocode(driver, url, data["cl1024"][0]["id"], data["cl1024"][0]["password"], CL_1024_PATH)
        #if platform.system() == "Linux":
        #    driver.close()
        #analyze_link(CL_1024_PATH, driver)
        ranking(CL_1024_PATH, 100)
    except:
        driver.close()
    #analyze_link(CL_1024_PATH, driver)
    driver.close()


main()
