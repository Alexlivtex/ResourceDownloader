import requests
import bs4 as bs
import os
import pickle
import shutil

pickle_data = os.path.join("file_config", "bt_download", "hub_hash_total.pickle")
pickle_data_bak = os.path.join("file_config", "bt_download", "hub_hash_total_bak.pickle")

start_url = os.path.join("file_config", "bt_download", "url_start_here")

total_hash_list = []

def extract_link(url):
    response = requests.get(url)
    # print(response.content)
    soup = bs.BeautifulSoup(response.content, "lxml")
    for a in soup.find_all('a', href=True):
        if len(a['href'].split("viewkey=")) > 1:
            hash_value = (a['href'].split("viewkey="))[-1][:15]
            if not hash_value in total_hash_list:
                total_hash_list.append(hash_value)
                if len(total_hash_list) % 50 == 0:
                    f_hash_total = open(pickle_data, "wb")
                    pickle.dump(total_hash_list, f_hash_total)
                    f_hash_total.close()
                    shutil.copy(pickle_data, pickle_data_bak)



def begin_hub_download():
    global total_hash_list
    url_video_prefix = ""
    if os.path.exists(pickle_data):
        try:
            f_hash_total = open(pickle_data, "rb")
            total_has_list = pickle.load(f_hash_total)
            f_hash_total.close()
        except:
            f_hash_total = open(pickle_data_bak, "rb")
            total_has_list = pickle.load(f_hash_total)
            f_hash_total.close()
    else:
        f_url_list = open(start_url)
        url_lines = f_url_list.readlines()
        for url_line in url_lines:
            extract_link(url_line)
        f_url_list.close()

    f_url_list = open(start_url)
    url_lines = f_url_list.readlines()
    url_video_prefix = url_lines[0].split("viewkey=")[0]
    f_url_list.close()

    for hash_index in total_hash_list:
        link = url_video_prefix + "viewkey=" + hash_index
        print(link)


begin_hub_download()


