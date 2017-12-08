from __future__ import unicode_literals
import requests
import bs4 as bs
import os
import pickle
import shutil
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join("file_download", "phub_download", "%(title)s")
}

MAX_DOWNLOAD_COUNT = 10

pickle_data = os.path.join("file_config", "bt_download", "hub_hash_total.pickle")
pickle_data_bak = os.path.join("file_config", "bt_download", "hub_hash_total_bak.pickle")

pickle_finished = os.path.join("file_config", "bt_download", "hub_finished_download.pickle")
pickle_finished_bak = os.path.join("file_config", "bt_download", "hub_finished_download_bak.pickle")

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
    download_count = 0
    finished_download_list = []

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

    if os.path.exists(pickle_finished):
        f_finished = open(pickle_finished, "rb")
        finished_download_list = pickle.load(f_finished)
        f_finished.close()

    f_url_list = open(start_url)
    url_lines = f_url_list.readlines()
    url_video_prefix = url_lines[0].split("viewkey=")[0]
    f_url_list.close()

    for hash_index in total_hash_list:
        link = url_video_prefix + "viewkey=" + hash_index
        if not link in finished_download_list and download_count < MAX_DOWNLOAD_COUNT:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            except:
                print("{} seems has an error in it".format(link))
                continue
            download_count += 1
            finished_download_list.append(link)


    f_finished = open(pickle_finished, "wb")
    pickle.dump(finished_download_list, f_finished)
    f_finished.close()
    shutil.copy(pickle_finished, pickle_finished_bak)


begin_hub_download()


