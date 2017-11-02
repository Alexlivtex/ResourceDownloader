from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from check_disk_status import check_disk_percentage
from post_deal_process import post_process
from pre_check_process import pre_check_net_disk
import urllib2
import requests
import os
import shutil
import pickle

total_list = {}
total_pickle_path = os.path.join("file_config", "learning_markets", "total.pickle")

finished_list = []
finished_pickle_path = os.path.join("file_config", "learning_markets", "finished.pickle")

video_download_path = os.path.join("file_download", "learning_markets_video")

net_disk_list = []
net_disk_pickle_path = os.path.join("file_config", "learning_markets", "learning_markets_net_map.pickle")

def as_num(x):
    y='{:.5f}'.format(x)
    return(y)

def download_file(url, file_name, ori_name):
    global finished_list
    r = requests.get(url, stream=True)
    total_size = requests.head(url).headers['content-length']
    current_download_index = 0
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                current_download_index += 1
                if current_download_index % (1024*5) == 0:
                    download_percent = (current_download_index * 1024) / float(total_size)
                    print("{} has already downloaded {}".format(ori_name, str(download_percent * 100)[:6] + "%"))
    print("{} has already downloaded {}".format(ori_name, str(100) + "%"))
    print(current_download_index)
    print(total_size)
    if not file_name in finished_list:
        finished_list.append(file_name)
    f_pickle = open(finished_pickle_path, "wb")
    pickle.dump(finished_list, f_pickle)
    f_pickle.close()
    f.close()

def start_extract_learning_markets(update=True):
    global finished_list
    global total_list
    global net_disk_list

    if os.path.exists(finished_pickle_path):
        f_pickle = open(finished_pickle_path, "rb")
        finished_list = pickle.load(f_pickle)
        f_pickle.close()

    if os.path.exists(total_pickle_path):
        f_total = open(total_pickle_path, "rb")
        total_list = pickle.load(f_total)
        f_total.close()

    if os.path.exists(net_disk_pickle_path):
        f_net_disk = open(net_disk_pickle_path, "rb")
        net_disk_list = pickle.load(f_net_disk)
        f_net_disk.close()

    if update is True:
        driver = webdriver.Firefox()
        driver.get("https://www.learningmarkets.com/strategy-sessions/")
        # buttont_elem = driver.find_element_by_class_name("btn btn-default dropdown-toggle")
        buttont_elem = driver.find_element_by_css_selector(".btn.btn-default.dropdown-toggle")
        buttont_elem.click()

        # subitem = driver.find_element_by_css_selector(".dropdown-menu.pull-right")
        li_list = driver.find_elements_by_css_selector(".dropdown-item.dropdown-item-button")
        for li_item in li_list:
            if li_item.text == "All":
                li_item.click()
                break

        link_list = driver.find_elements_by_tag_name("a")

        for link_item in link_list:
            if link_item.text == "view":
                print(link_item.get_attribute("href"))
                soup = BeautifulSoup(urllib2.urlopen(link_item.get_attribute("href")), "html5lib")
                video_link = soup.find_all("source")[0]["src"]
                print(video_link)
                file_name = link_item.get_attribute("href").split("/")[-2] + ".mp4"
                originan_name = file_name
                url = video_link[:-4]
                original_file_name = url.split("/")[-1]
                original_file_name = original_file_name.split(".")[0]
                year = original_file_name.split("-")[-2]
                month = original_file_name.split("-")[0][2:]
                day = original_file_name.split("-")[1]
                time_stap = year + "-" + month + "-" + day + "-"
                file_name = time_stap + file_name
                file_name = os.path.join(video_download_path, file_name)
                print(file_name)
                print(url)
                try:
                    #download_file(url, file_name, originan_name)
                    if url in total_list:
                        print("{} has already in the total list".format(url))
                        continue
                    else:
                        total_list[url] = [file_name, originan_name]
                except:
                    print("{} download has some error, skip it!".format(originan_name))
                    continue
        f_total = open(total_pickle_path, "wb")
        pickle.dump(total_list, f_total)
        f_total.close()
        driver.quit()

    else:
        if os.path.exists(total_pickle_path):
            f_total = open(total_pickle_path, "rb")
            total_list = pickle.load(f_total)
            f_total.close()
            for net_disk_index in net_disk_list:
                if os.path.exists(os.path.join(video_download_path, net_disk_index)):
                    print("{} has already existed in net disk, so delete it".format(os.path.join(video_download_path, net_disk_index)))
                    os.remove(os.path.join(video_download_path, net_disk_index))

            for total_dic_index in total_list:
                file_name = total_list[total_dic_index][0]
                originan_name = total_list[total_dic_index][1]
                percent = check_disk_percentage()
                if percent > 0.70:
                    print("No enough disk space left!")
                    post_process()
                    pre_check_net_disk()

                    if os.path.exists(net_disk_pickle_path):
                        f_net_disk = open(net_disk_pickle_path, "rb")
                        net_disk_list = pickle.load(f_net_disk)
                        f_net_disk.close()

                if file_name.split("/")[-1] in net_disk_list:
                    print("{} has already existed in net disk".format(file_name))
                    continue

                if file_name in finished_list and os.path.exists(file_name):
                    print("{} has already exsited".format(originan_name))
                    continue
                download_file(total_dic_index, file_name, originan_name)
