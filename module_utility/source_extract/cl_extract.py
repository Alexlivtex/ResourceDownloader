import bs4 as bs
import time
import io
import sys
import pickle
import os
import shutil
import threading
import platform
import requests
import operator

TOTAL_NOCODE_PICKLE = "nocode.pickle"
TOTAL_NOCODE_PICKLE_BAK = "nocode_bak.pickle"

TOTAL_NOCODE_ERROR = "nocode_error.pickle"

TOTAL_NOCODE_DIC = {}

if platform.system() == "Windows":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.setrecursionlimit(10000000)

section_map = {"NOCODE_ASIA" : 2,
               "CODE_ASIA" : 15,
               "EURA" : 4,
               "COMIC" : 5,
               "NATION_MADE" : 25,
               "CH_SUB" : 26,
               "EXCHANGE" : 27,
               "HTTP":21,
               "ONLINE" : 22,
               "LIBRARY" : 10,
               "TECH_DISCUSS" : 7,
               "NEW_GEN" : 8,
               "DAGGLE" : 16,
               "LITERATUAL" : 20
               }

def ranking(config_path, ranking_count):
    full_dic = {}
    with open(os.path.join(config_path, TOTAL_NOCODE_PICKLE), "rb") as f:
        full_dic = pickle.load(f)

    sorted_x = sorted(full_dic.items(), key=operator.itemgetter(3))
    print(sorted_x[:ranking_count])

def analyze_link(config_path, driver):
    global TOTAL_NOCODE_DIC
    TOTAL_ERROR_LIST = list()

    if os.path.exists(os.path.join(config_path, TOTAL_NOCODE_PICKLE)):
        with open(os.path.join(config_path, TOTAL_NOCODE_PICKLE), "rb") as f:
            TOTAL_NOCODE_DIC = pickle.load(f)

    if os.path.exists(os.path.join(config_path, TOTAL_NOCODE_ERROR)):
        with open(os.path.join(config_path, TOTAL_NOCODE_ERROR), "rb") as f:
            TOTAL_ERROR_LIST = pickle.load(f)

    loop_counter = 1
    for item_index in TOTAL_NOCODE_DIC:
        time.sleep(1)
        sys.stdout.flush()
        try:
            if platform.system() == "Windows":
                driver.get(item_index)
            else:
                r = requests.get(item_index)
        except:
            TOTAL_ERROR_LIST.append(str(item_index))
            with open(os.path.join(os.path.join(config_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        if platform.system() == "Windows":
            page_source = str(driver.page_source)
        else:
            page_source = str(r.content)
        #print(page_source)
        print("-" * 150)
        print(item_index)
        start_index = page_source.rfind("rmdown.com")
        if start_index < 0:
            TOTAL_ERROR_LIST.append(str(item_index))
            with open(os.path.join(os.path.join(config_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        end_index = start_index
        print(start_index)
        while True:
            if(page_source[start_index] == ">"):
                start_index += 1
                break
            start_index -= 1
        while True:
            if(page_source[end_index] == "<"):
                break
            end_index += 1
        torrent_link = page_source[start_index : end_index]
        try:
            if platform.system() == "Windows":
                driver.get(torrent_link)
            else:
                r = requests.get(torrent_link)
        except:
            TOTAL_ERROR_LIST.append(str(item_index))
            with open(os.path.join(os.path.join(config_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        if platform.system() == "Windows":
            torrent_link_source = str(driver.page_source)
        else:
            torrent_link_source = str(r.content)

        start_index = torrent_link_source.find("Downloaded")
        if start_index < 0:
            TOTAL_ERROR_LIST.append(str(item_index))
            with open(os.path.join(os.path.join(config_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        while True:
            if torrent_link_source[start_index].isdigit():
                break
            start_index += 1

        end_index = start_index
        while True:
            if not torrent_link_source[end_index].isdigit():
                break
            end_index += 1

        if "hash" not in torrent_link:
            download_count = 0
        else:
            download_count = int(torrent_link_source[start_index:end_index].strip())
        print("Torrent link : {}".format(torrent_link))
        print("Downloaded count : {}".format(download_count))
        print("*" * 150)
        TOTAL_NOCODE_DIC[item_index]["TorrentLink"] = torrent_link
        TOTAL_NOCODE_DIC[item_index]["DownloadingCount"] = download_count

        if loop_counter % 10 == 0:
            with open(os.path.join(config_path, TOTAL_NOCODE_PICKLE), "wb") as f:
                pickle.dump(TOTAL_NOCODE_DIC, f)

        if loop_counter % 30 == 0:
            shutil.copy(os.path.join(config_path, TOTAL_NOCODE_PICKLE), os.path.join(config_path, TOTAL_NOCODE_PICKLE_BAK))

        loop_counter += 1

def extract_source_asis_nocode(driver, url, id, passwd, data_path):
    global  TOTAL_NOCODE_DIC
    TOTAL_ERROR_LIST = list()
    login_url = "http://t66y.com/login.php"

    driver.set_page_load_timeout(50)
    driver.set_script_timeout(50)
    driver.get(login_url)

    elem_user_name = driver.find_element_by_name("pwuser")
    elem_user_pasword = driver.find_element_by_name("pwpwd")
    elem_user_name.send_keys(id)
    elem_user_pasword.send_keys(passwd)
    elem_login = driver.find_element_by_name("submit")
    time.sleep(3)
    elem_login.click()
    time.sleep(2)

    driver.get(url + "/thread0806.php?fid=" + str(section_map["NOCODE_ASIA"]) + "&search=&page=0")
    soup = bs.BeautifulSoup(driver.page_source, "lxml")
    page_total = soup.findAll("input")[0]["onblur"]
    total_page_count = page_total.split("=")[-1].split("/")[-1].split("'")[0]

    if os.path.exists(os.path.join(data_path, TOTAL_NOCODE_PICKLE)):
        with open(os.path.join(data_path, TOTAL_NOCODE_PICKLE), "rb") as f:
            TOTAL_NOCODE_DIC = pickle.load(f)
    else:
        f = open(os.path.join(data_path, TOTAL_NOCODE_PICKLE), "wb")
        pickle.dump(TOTAL_NOCODE_DIC, f)
        f.close()

    if os.path.exists(os.path.join(data_path, TOTAL_NOCODE_ERROR)):
        with open(os.path.join(data_path, TOTAL_NOCODE_ERROR), "rb") as f:
            TOTAL_ERROR_LIST = pickle.load(f)
            
    for index in range(1, int(total_page_count)):
        time.sleep(1)
        print("*********************************Current page index is : {}*********************************".format(index))
        complete_url = url + "/thread0806.php?fid=" + str(section_map["NOCODE_ASIA"]) + "&search=&page=" + str(index)
        try:
            driver.get(complete_url)
        except:
            continue
        source = driver.page_source
        soup = bs.BeautifulSoup(source, "lxml")
        for sub_item in soup.findAll("h3"):
            if len(sub_item.findAll('a')) == 0:
                TOTAL_ERROR_LIST.append(str(sub_item))
                with open(os.path.join(os.path.join(data_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                    pickle.dump(TOTAL_ERROR_LIST, f)
                continue
            link = sub_item.findAll('a')[0]
            title = link.text
            try:
                full_link = "/".join(login_url.split('/')[:-1]) + '/' + link["href"]
            except:
                print(link)
                TOTAL_ERROR_LIST.append(str(sub_item))
                with open(os.path.join(os.path.join(data_path, TOTAL_NOCODE_ERROR)), "wb") as f:
                    pickle.dump(TOTAL_ERROR_LIST, f)
                continue
            #print("-" * 100)
            if full_link in TOTAL_NOCODE_DIC:
                print("{} has already exixts".format(full_link))
                continue
            if "htm_data" not in full_link:
                print("Invalid link")
                continue

            print("link : {}".format(full_link))
            if platform.system() == "Windows":
                print("Title : {}".format(title))

            item = {"Title" : title, "TorrentLink" : "", "DownloadingCount" : 0}
            TOTAL_NOCODE_DIC[full_link] = item

            #print(TOTAL_NOCODE_DIC)
            if len(TOTAL_NOCODE_DIC) % 10 == 0:
                with open(os.path.join(data_path, TOTAL_NOCODE_PICKLE), "wb") as f:
                    pickle.dump(TOTAL_NOCODE_DIC, f)

            if len(TOTAL_NOCODE_DIC) % 30 == 0:
                shutil.copy(os.path.join(data_path, TOTAL_NOCODE_PICKLE), os.path.join(data_path, TOTAL_NOCODE_PICKLE_BAK))

