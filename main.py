from module_utility.learning_markets.video_download import start_extract_learning_markets

def main():
    #Download the latest learning markets video
    start_extract_learning_markets(True)
    start_extract_learning_markets(False)

main()
