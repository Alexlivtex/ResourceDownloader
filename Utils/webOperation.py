import platform
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def openBrowser():
    driver_path = os.path.join("files", "webdriver")
    if platform.system() == "Windows":
        driver = webdriver.Chrome(os.path.join(driver_path, "Windows", "chromedriver.exe"))
    else:
        binary = FirefoxBinary(os.path.join(driver_path, "Linux", "geckodriver"))
        driver = webdriver.Firefox(firefox_binary=binary)
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--dns-prefetch-disable")
        driver = webdriver.Chrome(os.path.join(driver_path, "Linux", "chromedriver"),chrome_options=options)
        '''
    time.sleep(5)
    return driver
