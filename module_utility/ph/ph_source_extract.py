import requests
import bs4 as bs
import os
import pickle
import time
import shutil


def extract_link(configList):
    data_total = {}
    error_total = []

    url = configList["url"]
    data_name = configList["data_name"]
    data_name_bak = configList["data_bak_name"]
    data_name_error = configList["data_error_name"]
    count_times = configList["count_times"]

    if os.path.exists(data_name):
        with open(data_name, "rb") as f:
            data_total = pickle.load(f)

    if os.path.exists(data_name_error):
        with open(data_name_error, "rb") as f:
            error_total = pickle.load(f)

    page_index = 1
    hasNextPage = True
    while hasNextPage:
        response = requests.get(url + "video?page=" + str(page_index))
        soup = bs.BeautifulSoup(response.content, "lxml")
        index = len(soup.find_all('img', {"class", "pagination_arrow_right"}))
        if index == 0:
            hasNextPage = False
        else:
            hasNextPage = True

        for a in soup.find_all('a', href=True):
            if len(a['href'].split("viewkey=")) > 1:
                hash_value = (a['href'].split("viewkey="))[-1]
                print(hash_value)
                try:
                    sub_response = requests.get(url + "view_video.php?viewkey=" + hash_value)
                    print(url + "view_video.php?viewkey=" + hash_value)
                    sub_soup = bs.BeautifulSoup(sub_response.content, "lxml")
                except:
                    print("{} has some error".format(hash_value))
                    if not hash_value in error_total:
                        error_total.append(hash_value)
                    continue
                # viewCount = soup.find_all('span', {'class': 'count'})[0].text
                if len(sub_soup.find_all('span', {'class': 'count'})) > 0:
                    viewCount = sub_soup.find_all('span', {'class': 'count'})[0].text
                else:
                    print("{} has some error".format(hash_value))
                    if not hash_value in error_total:
                        error_total.append(hash_value)
                    continue
                viewCount = "".join(viewCount.split(','))
                data_total[hash_value] = viewCount

                if len(data_total) % 10 == 0:
                    with open(data_name, "wb") as f:
                        pickle.dump(data_total, f)

                    if len(data_name_error) > 0:
                        with open(data_name_error, "wb") as f:
                            pickle.dump(data_name_error, f)

                    shutil.copy(data_name, data_name_bak)
                print("************************{} has viewed  {} times************************".format(hash_value, viewCount))
        print("======Now getting page {}======".format(url + "video?page=" + str(page_index)))
        page_index += 1
        time.sleep(1)
