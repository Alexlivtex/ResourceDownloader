from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.post_deal_process import post_process
from bypy import ByPy
from module_utility.timeout import timeout
import os

MAX_TIME_LEARNING_MARKETS = 15*60
MAX_TIME_BT_DOWNLOAD = 45*60

@timeout(MAX_TIME_LEARNING_MARKETS)
def upload_learning_markets(path):
    bp = ByPy()
    bp.upload(path)

def main():
    #Download the latest learning markets video
    start_extract_learning_markets(True)
    start_extract_learning_markets(False)
    while True:
        try:
            upload_learning_markets("file_download")
            post_process()
            break
        except:
            continue

main()
