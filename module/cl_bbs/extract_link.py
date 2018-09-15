import sys
import time
import platform
import requests


def analyze_link_torrent(driver, paramList):
    TOTAL_ERROR_LIST = list()
    TOTAL_DATA_DIC = dict()

    loop_counter = 1
    for item_index in TOTAL_DATA_DIC:
        time.sleep(1)
        sys.stdout.flush()
        try:
            if platform.system() == "Windows":
                driver.get(item_index)
            else:
                r = requests.get(item_index)
        except:
            TOTAL_ERROR_LIST.append(str(item_index))
            continue
        if platform.system() == "Windows":
            page_source = str(driver.page_source)
        else:
            page_source = str(r.content)
        # print(page_source)
        print("-" * 150)
        print(item_index)
        start_index = page_source.rfind("rmdown.com")
        if start_index < 0:
            TOTAL_ERROR_LIST.append(str(item_index))
            continue
        end_index = start_index
        print(start_index)
        while True:
            if (page_source[start_index] == ">"):
                start_index += 1
                break
            start_index -= 1
        while True:
            if (page_source[end_index] == "<"):
                break
            end_index += 1
        torrent_link = page_source[start_index: end_index]
        try:
            if platform.system() == "Windows":
                driver.get(torrent_link)
            else:
                r = requests.get(torrent_link)
        except:
            TOTAL_ERROR_LIST.append(str(item_index))
            continue
        if platform.system() == "Windows":
            torrent_link_source = str(driver.page_source)
        else:
            torrent_link_source = str(r.content)

        start_index = torrent_link_source.find("Downloaded")
        if start_index < 0:
            TOTAL_ERROR_LIST.append(str(item_index))
            continue
        while True:
            if torrent_link_source[start_index].isdigit():
                break
            if torrent_link_source[start_index] == "<":
                TOTAL_ERROR_LIST.append(str(item_index))
                start_index = -1
                break
            start_index += 1

        end_index = start_index
        while True:
            if end_index == -1:
                break
            if not torrent_link_source[end_index].isdigit():
                break
            end_index += 1

        if "hash" not in torrent_link or start_index == -1:
            download_count = 0
        else:
            download_count = int(torrent_link_source[start_index:end_index].strip())
        print("Torrent link : {}".format(torrent_link))
        print("Downloaded count : {}".format(download_count))
        print("*" * 150)
        TOTAL_DATA_DIC[item_index]["TorrentLink"] = torrent_link
        TOTAL_DATA_DIC[item_index]["DownloadingCount"] = download_count

        loop_counter += 1