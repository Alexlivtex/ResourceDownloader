from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.post_deal_process import post_process
from module_utility.bt_download.video_download import begin_download
from module_utility.bt_download.data_update3 import analysis_website
from module_utility.bt_download.data_update3 import get_torrent_link
from bypy import ByPy
from selenium import webdriver
import os

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

MAX_TIME_LEARNING_MARKETS = 15*60
MAX_TIME_BT_DOWNLOAD = 15*60
MAX_TIME_UPLOAD_SLEEP = 5*60


def main():
    '''
    #Download the latest learning markets video
    @timeout(MAX_TIME_LEARNING_MARKETS)
    def upload_learning_markets(path):
        bp = ByPy()
        bp.upload(path)

    try:
        start_extract_learning_markets()
    except:
        print("Skip this function, got to the next one!")

    while True:
        try:
            upload_learning_markets("file_download")
            post_process()
            break
        except:
            print("First try upload failed, try again!")
            continue
    '''

    if download_times % 6 == 0:
        # Get all the data link from the websites
        while True:
            try:
                web_driver = webdriver.Firefox()
                analysis_website(web_driver)
                web_driver.quit()
                break
            except:
                try:
                    web_driver.quit()
                except:
                    print("Error happened when close the browser")

        time.sleep(5 * 60)

        # Get all the data link from the websites
        while True:
            try:
                web_driver = webdriver.Firefox()
                get_torrent_link(web_driver)
                web_driver.quit()
                break
            except:
                try:
                    web_driver.quit()
                except:
                    print("Error happened when quit the driver")


        time.sleep(5 * 60)

    #Download the download the bt video
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
            os.system("rm -rf file_download/bt_download/download_dir/*")
            break
        except:
            print("Upload video failed, try again!")
            continue

while True:
    try:
        if os.path.exists(pickle_downloading_times):
            f_downloading = open(pickle_downloading_times, "rb")
            download_times = pickle.load(f_downloading)
            f_downloading.close()

        main()
        download_times += 1

        f_downloading = open(pickle_downloading_times, "wb")
        pickle.dump(download_times, f_downloading)
        f_downloading.close()
    except:
        print("Unknown error happened! Continue to execute")
        time.sleep(10*60)
        continue
