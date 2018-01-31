from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.post_deal_process import post_process
from module_utility.bt_download.video_download import begin_download
from module_utility.bt_download.data_update3 import analysis_website
from module_utility.bt_download.data_update3 import get_torrent_link
from module_utility.phub_download.video_download import begin_hub_download
from module_utility.bt_download.torrent_transform import transform
from bypy import ByPy
from selenium import webdriver
import os
import shutil

from functools import wraps
import errno
import os
import signal
import time
import pickle

download_times = 2

pickle_downloading_times = os.path.join("file_config", "bt_download", "downloading_times.pickle")

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

MAX_TIME_BT_DOWNLOAD = 15*60
MAX_TIME_UPLOAD_SLEEP = 5*60


def main():
    #####1st Get the torrent link
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")


    driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=options)
    #driver = webdriver.Chrome("D:\Chrome_Download\chromedriver_win32\chromedriver.exe")
    #analysis_website(driver)
    try:
        driver.close()
    except:
        print("Session has already released")

    time.sleep(30)
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    get_torrent_link(driver)
    try:
        driver.close()
    except:
        print("Session has already released")

    transform()
    
    
    ##### 2nd Download the download the bt video
    @timeout(MAX_TIME_BT_DOWNLOAD)
    def upload_bt_download(path):
        bp = ByPy()
        bp.upload(path)
        bp.cleancache()

    begin_hub_download()
    while True:
        try:
            time.sleep(MAX_TIME_UPLOAD_SLEEP)
            upload_bt_download("file_download")
            #os.system("rm -rf file_download/phub_download/*")
            shutil.rmtree(os.path.join("file_download", "phub_download"))
            os.mkdir(os.path.join("file_download", "phub_download"))
            break
        except:
            print("phub upload video failed, try again!")
            continue


    ##### 3rd Download the download the bt video
    @timeout(MAX_TIME_BT_DOWNLOAD)
    def upload_bt_download(path):
        bp = ByPy()
        bp.upload(path)
        bp.cleancache()

    begin_download()
    while True:
        try:
            time.sleep(MAX_TIME_UPLOAD_SLEEP)
            upload_bt_download("file_download")
            #os.system("rm -rf file_download/bt_download/download_dir/*")
            shutil.rmtree(os.path.join("file_download", "bt_download", "download_dir"))
            os.mkdir(os.path.join("file_download", "bt_download", "download_dir"))
            break
        except:
            print("Upload video failed, try again!")
            continue


#while True:
#    try:
main()
#    except:
#        print("Unknown error happened! Continue to execute")
#        time.sleep(10*60)
#        continue
