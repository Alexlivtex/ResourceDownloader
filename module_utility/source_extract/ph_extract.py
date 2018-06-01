import pickle
import os
import platform
import requests
import bs4 as bs
import time
import sys

def extract_ph_source(driver, paramList):
    url_data_base = dict()
    url_error_list = list()
    url = paramList["url"]
    viewKey = paramList["viewKey"]
    data_name = paramList["data_name"]
    data_name_bak = paramList["data_name_bak"]
    data_name_error = paramList["data_name_error"]

    if os.path.exists(data_name):
        with open(data_name, "rb") as f:
            url_data_base = pickle.load(f)
    else:
        url_data_base[url + "/view_video.php?viewkey=" + viewKey] = 0

    if os.path.exists(data_name_error):
        with open(data_name_error) as f:
            url_error_list = pickle.load(f)

    for item in url_data_base:
        try:
            if platform.system() == "Windows":
                driver.get(item)
            else:
                r = requests.get(item)
        except:
            if not item in url_error_list:
                url_error_list.append(item)
                continue

        if platform.system() == "Windows":
            page_source = str(driver.page_source)
        else:
            page_source = str(r.content)

        soup = bs.BeautifulSoup(page_source, "lxml")
        viewCount = soup.find_all('span', {'class' : 'count'})[0].text
        viewCount = "".join(viewCount.split(','))
        sys.stdout.flush()
        print(viewCount)
        time.sleep(500)
