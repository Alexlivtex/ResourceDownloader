from module_utility.learning_markets.video_download import start_extract_learning_markets
from module_utility.learning_markets.pre_check_process import pre_check_net_disk



def main():
    pre_check_net_disk()
    #Download the latest learning markets video
    start_extract_learning_markets(True)
    start_extract_learning_markets(False)

main()
