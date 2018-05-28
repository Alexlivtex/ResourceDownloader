import bs4 as bs
import time
import io
import sys
import pickle
import os
import shutil
import platform
import requests

import xml.etree.cElementTree as ET
from time import gmtime, strftime

if platform.system() == "Windows":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.setrecursionlimit(10000000)

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def gen_counting_list(file_name, data, dataCount):
    downloadingInfo = ET.Element("DownloadInfo")
    downloadingInfo.set("MaxAmount", str(dataCount))
    downloadingInfo.set("ModifyTime", strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    for item in data:
        subnode = ET.SubElement(downloadingInfo, "SubItem")
        Title = ET.SubElement(subnode, "Title")
        MainLink = ET.SubElement(subnode, "Link")
        DownloadCount = ET.SubElement(subnode, "Downloaded")
        Link = ET.SubElement(subnode, "TorrentLink")

        Title.text = str(item[1]['Title'])
        MainLink.text = str(item[0])
        DownloadCount.text = str(item[1]['DownloadingCount'])
        Link.text = item[1]['TorrentLink']

    indent(downloadingInfo)
    tree = ET.ElementTree(downloadingInfo)
    tree.write(file_name, xml_declaration=True, encoding='utf-8', method="xml")

def ranking(paramList):
    data = paramList["data"]
    ranking_count = paramList["counting"]
    full_dic = {}
    count_xml = data.split(".")[0] + ".xml"
    with open(data, "rb") as f:
        full_dic = pickle.load(f)

    sorted_x = sorted(full_dic.items(), key=lambda x : x[1]['DownloadingCount'], reverse=True)
    link_list = []
    sortedData = sorted_x[:ranking_count * 2]
    for item in sortedData:
        linkUrl = item[1]['TorrentLink']
        if linkUrl in link_list:
            sortedData.remove(item)
        else:
            link_list.append(linkUrl)
    gen_counting_list(count_xml, sortedData[:ranking_count], ranking_count)

def analyze_link_torrent(driver, paramList):
    TOTAL_ERROR_LIST = list()
    TOTAL_DATA_DIC = dict()
    data = paramList["data"]
    errorData = paramList["errorData"]
    bakData = paramList["bakData"]

    if os.path.exists(data):
        with open(data, "rb") as f:
            TOTAL_DATA_DIC = pickle.load(f)

    if os.path.exists(errorData):
        with open(errorData, "rb") as f:
            TOTAL_ERROR_LIST = pickle.load(f)

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
            with open(errorData, "wb") as f:
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
            with open(errorData, "wb") as f:
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
            with open(errorData, "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        if platform.system() == "Windows":
            torrent_link_source = str(driver.page_source)
        else:
            torrent_link_source = str(r.content)

        start_index = torrent_link_source.find("Downloaded")
        if start_index < 0:
            TOTAL_ERROR_LIST.append(str(item_index))
            with open(errorData, "wb") as f:
                pickle.dump(TOTAL_ERROR_LIST, f)
            continue
        while True:
            if torrent_link_source[start_index].isdigit():
                break
            if torrent_link_source[start_index] == "<":
                TOTAL_ERROR_LIST.append(str(item_index))
                with open(errorData, "wb") as f:
                    pickle.dump(TOTAL_ERROR_LIST, f)
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

        if loop_counter % 10 == 0:
            with open(data, "wb") as f:
                pickle.dump(TOTAL_DATA_DIC, f)

        if loop_counter % 30 == 0:
            shutil.copy(data, bakData)

        if loop_counter % 50 == 0:
            ranking(paramList)

        loop_counter += 1

def extract_source_torrent(driver, paramList):
    TOTAL_ERROR_LIST = list()
    TOTAL_DATA_DIC = dict()
    url = paramList["url"]
    #id = paramList["id"]
    #passwd = paramList["passwd"]
    data = paramList["data"]
    errorData = paramList["errorData"]
    bakData = paramList["bakData"]
    section = paramList["section"]

    login_url = url + "/login.php"

    #driver.set_page_load_timeout(50)
    #driver.set_script_timeout(50)
    #driver.get(login_url)

    #elem_user_name = driver.find_element_by_name("pwuser")
    #elem_user_pasword = driver.find_element_by_name("pwpwd")
    #elem_user_name.send_keys(id)
    #elem_user_pasword.send_keys(passwd)
    #elem_login = driver.find_element_by_name("submit")
    #time.sleep(3)
    #elem_login.click()
    #time.sleep(2)

    driver.get(url + "/thread0806.php?fid=" + str(section) + "&search=&page=0")
    soup = bs.BeautifulSoup(driver.page_source, "lxml")
    page_total = soup.findAll("input")[0]["onblur"]
    total_page_count = page_total.split("=")[-1].split("/")[-1].split("'")[0]

    if os.path.exists(data):
        with open(data, "rb") as f:
            TOTAL_DATA_DIC = pickle.load(f)
    else:
        f = open(data, "wb")
        pickle.dump(TOTAL_DATA_DIC, f)
        f.close()

    if os.path.exists(errorData):
        with open(errorData, "rb") as f:
            TOTAL_ERROR_LIST = pickle.load(f)
            
    for index in range(1, int(total_page_count)):
        time.sleep(1)
        print("*********************************Current page index is : {}*********************************".format(index))
        complete_url = url + "/thread0806.php?fid=" + str(section) + "&search=&page=" + str(index)
        try:
            driver.get(complete_url)
        except:
            continue
        source = driver.page_source
        soup = bs.BeautifulSoup(source, "lxml")
        for sub_item in soup.findAll("h3"):
            if len(sub_item.findAll('a')) == 0:
                TOTAL_ERROR_LIST.append(str(sub_item))
                with open(errorData, "wb") as f:
                    pickle.dump(TOTAL_ERROR_LIST, f)
                continue
            link = sub_item.findAll('a')[0]
            title = link.text
            try:
                full_link = "/".join(login_url.split('/')[:-1]) + '/' + link["href"]
            except:
                print(link)
                TOTAL_ERROR_LIST.append(str(sub_item))
                with open(errorData, "wb") as f:
                    pickle.dump(TOTAL_ERROR_LIST, f)
                continue
            #print("-" * 100)
            if full_link in TOTAL_DATA_DIC:
                print("{} has already exixts".format(full_link))
                continue
            if "htm_data" not in full_link:
                print("Invalid link")
                continue

            print("link : {}".format(full_link))
            if platform.system() == "Windows":
                print("Title : {}".format(title))

            item = {"Title" : title, "TorrentLink" : "", "DownloadingCount" : 0}
            TOTAL_DATA_DIC[full_link] = item

            #print(TOTAL_NOCODE_DIC)
            if len(TOTAL_DATA_DIC) % 10 == 0:
                with open(data, "wb") as f:
                    pickle.dump(TOTAL_DATA_DIC, f)

            if len(TOTAL_DATA_DIC) % 30 == 0:
                shutil.copy(data, bakData)

