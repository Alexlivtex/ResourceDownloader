from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.post_deal_process import post_process
from bypy import ByPy
import os

from functools import wraps
import errno
import os
import signal

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
MAX_TIME_BT_DOWNLOAD = 45*60

def main():
    #Download the latest learning markets video
    @timeout(MAX_TIME_LEARNING_MARKETS)
    def upload_learning_markets(path):
        bp = ByPy()
        bp.upload(path)

    start_extract_learning_markets()
    while True:
        try:
            upload_learning_markets("file_download")
            post_process()
            break
        except:
            print("First try upload failed, try again!")
            continue

main()
