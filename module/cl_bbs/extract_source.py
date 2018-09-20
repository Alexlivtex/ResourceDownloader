import bs4 as bs
import time
import random
import requests
from .login import login_website
from selenium.common.exceptions import TimeoutException

from Utils import DBHelper

def extract_source_torrent(base_url, db, table_name, section):
    TOTAL_ERROR_LIST = list()
    TOTAL_DATA_DIC = dict()

    webhandle = login_website(db)

    login_url = base_url + "/login.php"

    webhandle.get(base_url + "/thread0806.php?fid=" + str(section) + "&search=&page=0")
    soup = bs.BeautifulSoup(webhandle.page_source, "lxml")
    page_total = soup.findAll("input")[0]["onblur"]
    total_page_count = page_total.split("=")[-1].split("/")[-1].split("'")[0]
    cookies = webhandle.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    for index in range(1, int(total_page_count) + 1):
        time.sleep(random.randint(1, 10))
        print("*********************************Current page index is : {}*********************************".format(
            index))
        complete_url = base_url + "/thread0806.php?fid=" + str(section) + "&search=&page=" + str(index)
        try:
            webhandle.get(complete_url)
            #r = s.get(complete_url)
        except TimeoutException as ex:
            print(ex.msg)
            try:
                webhandle.get(complete_url)
            except:
                webhandle.close()
                webhandle = login_website(db)
                try:
                    webhandle.get(complete_url)
                except Exception as e:
                    print(e)
                    print("Skip this loop!")
                    continue

        source = webhandle.page_source
        #source = r.content
        soup = bs.BeautifulSoup(source, "lxml")
        for sub_item in soup.findAll("h3"):
            if len(sub_item.findAll('a')) == 0:
                TOTAL_ERROR_LIST.append(str(sub_item))
                continue
            link = sub_item.findAll('a')[0]
            title = link.text
            try:
                full_link = "/".join(login_url.split('/')[:-1]) + '/' + link["href"]
            except:
                print(link)
                TOTAL_ERROR_LIST.append(str(sub_item))
                continue
            # print("-" * 100)
            if full_link in TOTAL_DATA_DIC:
                print("{} has already exixts".format(full_link))
                continue
            if "htm_data" not in full_link:
                print("Invalid link")
                continue

            cursor = DBHelper.fetchData(db, "SELECT * FROM {} WHERE Link='{}'".format(table_name, full_link))
            if cursor.fetchone() != None:
                print("Record has already existed!")
                continue
            else:
                print("Title : {}".format(title))
                print("link : {}".format(full_link))
                print("\n")
                
                InsertSQL = u"INSERT INTO {} (Title, Link, Section, TorrentLink, DownloadingCount) VALUES (%s, %s, %s, %s, %s )".format(table_name)
                InsertData = (title, full_link, section, "", 0)
                try:
                    DBHelper.insert_table(db, InsertSQL, InsertData)
                except Exception as err:
                    print(err)
                    continue

    webhandle.close()



