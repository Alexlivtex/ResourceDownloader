from selenium import webdriver
import time
import bs4 as bs
import pickle
import os
import re
from selenium.webdriver.common.keys import Keys
from check_total_data import check_data

max_nocode_count = 2500

base_no_code_url = "http://t66y.com/thread0806.php?fid=2&search=&page="
login_url = "http://t66y.com/login.php"
base_url = "http://t66y.com"

pickle_data = os.path.join("file_config", "bt_download", "data_total.pickle")

def analysis_website(driver):
    total_dic_map = {}
    total_err_list = []
    driver.implicitly_wait(20)

    driver.get(login_url)
    soup = bs.BeautifulSoup(driver.page_source, "lxml")
    title_content = soup.findAll("title")[0].text
    if title_content == "Attention Required! | Cloudflare":
        print(title_content)
        time.sleep(30)
        return
    else:
        elem_user_name = driver.find_element_by_name("pwuser")
        elem_user_pasword = driver.find_element_by_name("pwpwd")
        elem_user_name.send_keys("alexlivtex")
        elem_user_pasword.send_keys("heisenberg1987")
        #time.sleep(5)
        elem_login = driver.find_element_by_name("submit")
        elem_login.click()

    if os.path.exists(pickle_data):
        f_data_pickle = open(pickle_data, "rb")
        total_dic_map = pickle.load(f_data_pickle)
        f_data_pickle.close()

    driver.set_script_timeout(5)
    driver.set_page_load_timeout(5)
    for page_index in range(max_nocode_count):
        url = base_no_code_url + str(page_index)
        try:
            driver.get(url)
        except:
            print("Execution time exceeded when loading the total page!")
        #time.sleep(2)
        page_list_content = bs.BeautifulSoup(driver.page_source).findAll("h3")
        for title_item in page_list_content:
            try:
                link = title_item.findAll("a")[0]
                title = link.text
                item_link = base_url + "/" + link['href']
                if item_link in total_dic_map:
                    print("{} has already exists".format(item_link))
                    continue
                try:
                    driver.get(item_link)
                except:
                    print("Execution time exceeded when loading sub page!")
                #time.sleep(2)
                item_soup = bs.BeautifulSoup(driver.page_source)
                title_content = item_soup.findAll("title")[0].text
                if title_content == "Attention Required! | Cloudflare":
                    #time.sleep(10)
                    f_error_list = open("error.txt", "w")
                    f_error_list.writelines(total_err_list)
                    f_error_list.close()
                    driver.quit()
                    return
                torrent_link = item_soup.body.findAll(text=re.compile('^http://www.rmdown.com'))
                if len(torrent_link) > 0 and len(torrent_link[0].split("=")) > 1:
                    hash_value = torrent_link[0].split("=")[-1]
                    hash_value = hash_value[-40:]
                    magnet_link = "magnet:?xt=urn:btih:" + str(hash_value)
                    print(item_link)
                    print(title)
                    print(magnet_link)

                    total_dic_map[item_link] = [title, magnet_link]
                    if len(total_dic_map) % 10 == 0:
                        f_pickle = open(pickle_data, "wb")
                        pickle.dump(total_dic_map, f_pickle)
                        f_pickle.close()
            except:
                print("{} has some error in it!".format(item_link))
                total_err_list.append(item_link + "\n")





while True:
    try:
        web_driver = webdriver.Firefox()
        check_data()
        analysis_website(web_driver)
        check_data()
    except:
        web_driver.quit()
        continue

'''
web_driver = webdriver.Firefox()
try:
    check_data()
    analysis_website(web_driver)
    check_data()
except:
    web_driver.quit()
web_driver.quit()
'''