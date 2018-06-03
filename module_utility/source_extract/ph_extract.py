import pickle
import os
import platform
import requests
import bs4 as bs
import time
import sys
import shutil

url_data_base = dict()
url_error_list = list()


def extract_link(url, url_base, data_name, bak_data_name, data_error_name):
    response = requests.get(url)
    # print(response.content)
    soup = bs.BeautifulSoup(response.content, "lxml")
    for a in soup.find_all('a', href=True):
        if len(a['href'].split("viewkey=")) > 1:
            hash_value = (a['href'].split("viewkey="))[-1][:15]
            try:
                sub_response = requests.get(url_base + "/view_video.php?viewkey=" + hash_value)
                print(url_base + "/view_video.php?viewkey=" + hash_value)
                sub_soup = bs.BeautifulSoup(sub_response.content, "lxml")
            except:
                url_error_list.append(hash_value)
                continue
            # viewCount = soup.find_all('span', {'class': 'count'})[0].text
            if len(sub_soup.find_all('span', {'class': 'count'})) > 0:
                viewCount = sub_soup.find_all('span', {'class': 'count'})[0].text
            else:
                if not hash_value in url_error_list:
                    url_error_list.append(hash_value)
                continue
            viewCount = "".join(viewCount.split(','))
            url_data_base[hash_value] = viewCount
            print("************************{} has viewed  {} times************************".format(hash_value,
                                                                                                   viewCount))
            if len(url_data_base) % 50 == 0:
                f_hash_total = open(data_name, "wb")
                pickle.dump(url_data_base, f_hash_total)
                f_hash_total.close()
                shutil.copy(data_name, bak_data_name)

                with open(data_error_name, "wb") as f:
                    pickle.dump(url_error_list, f)


def extract_ph_source(driver, paramList):
    global url_data_base
    global url_error_list

    url = paramList["url"]
    viewKey = paramList["viewKey"]
    data_name = paramList["data_name"]
    data_name_bak = paramList["data_name_bak"]
    data_name_error = paramList["data_name_error"]

    if os.path.exists(data_name):
        with open(data_name, "rb") as f:
            url_data_base = pickle.load(f)
    else:
        url_data_base[viewKey] = 0

    if os.path.exists(data_name_error):
        with open(data_name_error) as f:
            url_error_list = pickle.load(f)

    while True:
        for item in list(url_data_base):
            full_url = url + "/view_video.php?viewkey=" + item
            print(full_url)
            extract_link(full_url, url, data_name, data_name_bak, data_name_error)
            time.sleep(2)
        '''
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

        print(viewCount)
        '''
