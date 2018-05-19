import bs4 as bs
import time
import io
import sys
import pickle
import os
import shutil

TOTAL_NOCODE_PICKLE = "nocode.pickle"
TOTAL_NOCODE_PICKLE_BAK = "nocode_bak.pickle"

TOTAL_NOCODE_DIC = {}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

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

def extract_source_asis_nocode(driver, url, id, passwd, data_path):
    global  TOTAL_NOCODE_DIC
    login_url = "http://t66y.com/login.php"
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

    for index in range(1, int(total_page_count)):
        time.sleep(1)
        complete_url = url + "/thread0806.php?fid=" + str(section_map["NOCODE_ASIA"]) + "&search=&page=" + str(index)
        driver.get(complete_url)
        soup = bs.BeautifulSoup(driver.page_source, "lxml")
        for sub_item in soup.findAll("h3"):
            link = sub_item.findAll('a')[0]
            title = link.text
            full_link = "/".join(login_url.split('/')[:-1]) + '/' + link["href"]
            #print("-" * 100)
            if full_link in TOTAL_NOCODE_DIC:
                print("{} has already exixts".format(full_link))
                continue
            if "htm_data" not in full_link:
                print("Invalid link")
                continue

            print("link : {}".format(full_link))
            print("Title : {}".format(title))

            item = {"Title" : title, "TorrentLink" : "", "DownloadingCount" : 0}
            TOTAL_NOCODE_DIC[full_link] = item

            #print(TOTAL_NOCODE_DIC)
            if len(TOTAL_NOCODE_DIC) % 10 == 0:
                with open(os.path.join(data_path, TOTAL_NOCODE_PICKLE), "wb") as f:
                    pickle.dump(TOTAL_NOCODE_DIC, f)

            if len(TOTAL_NOCODE_DIC) % 30 == 0:
                shutil.copy(os.path.join(data_path, TOTAL_NOCODE_PICKLE), os.path.join(data_path, TOTAL_NOCODE_PICKLE_BAK))

