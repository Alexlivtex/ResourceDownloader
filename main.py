from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.post_deal_process import post_process



def main():
    #Download the latest learning markets video
    start_extract_learning_markets(True)
    start_extract_learning_markets(False)
    while True:
        try:
            post_process()
            break
        except:
            continue

main()
