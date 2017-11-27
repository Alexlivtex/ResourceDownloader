from selenium import webdriver
import time
import bs4 as bs
import pickle
import os
import re
from check_total_data import check_data

max_nocode_count = 2500

base_no_code_url = "http://t66y.com/thread0806.php?fid=2&search=&page="
login_url = "http://t66y.com/login.php"
base_url = "http://t66y.com"

pickle_data = os.path.join("file_config", "bt_download", "data_total.pickle")
pickle_url_data = os.path.join("file_config", "bt_download", "data_url_total.pickle")
pickle_error_data = os.path.join("file_config", "bt_download", "data_error_total.pickle")

def get_torrent_link(driver):
    driver.set_page_load_timeout(15)
    driver.set_script_timeout(15)
    total_data_url_list = []
    current_total_url_list = []
    total_data_dic = {}
    total_error_list = []

    if os.path.exists(pickle_error_data):
        f_error = open(pickle_error_data, "rb")
        total_error_list = pickle.load(f_error)
        f_error.close()

    if not os.path.exists(pickle_url_data):
        print("Data file not exists!")
        return
    else:
        print("Data file exists!")
        f_current_url = open(pickle_url_data, "rb")
        current_total_url_list = pickle.load(f_current_url)
        f_current_url.close()

    if os.path.exists(pickle_data):
        check_data()
        f_total_data = open(pickle_data, "rb")
        total_data_dic = pickle.load(f_total_data)
        f_total_data.close()
        for dic_index in total_data_dic:
            total_data_url_list.append(dic_index)

    for current_url_index in current_total_url_list:
        if current_url_index[0] in total_data_url_list:
            print("{} has already exists".format(current_url_index[0]))
        else:
            try:
                driver.get(current_url_index[0])
            except:
                print("Time exceed when loading the page")
            soup = bs.BeautifulSoup(driver.page_source, "lxml")
            # soup = bs.BeautifulSoup(requests.get(url).text, 'html.parser')
            torrent_link = soup.body.findAll(text=re.compile('^http://www.rmdown.com'))
            if len(torrent_link) > 0 and len(torrent_link[0]) > len("http://www.rmdown.com"):
                if len(torrent_link[0].split("=")) > 1:
                    hash_value = torrent_link[0].split("=")[-1]
                    hash_value = hash_value[-40:]
                    magnet_link = "magnet:?xt=urn:btih:" + str(hash_value)
                    print(current_url_index[0])
                    print(current_url_index[1])
                    print(magnet_link)

                    total_data_dic[current_url_index[0]] = [current_url_index[1], magnet_link]
                    if len(total_data_dic) % 10 == 0:
                        f_pickle = open(pickle_data, "wb")
                        pickle.dump(total_data_dic, f_pickle)
                        f_pickle.close()
            else:
                print("Cant not find the torrent link for {}".format(current_url_index[0]))
                if not current_url_index[0] in total_error_list:
                    total_error_list.append(current_url_index[0])
                    if len(total_error_list) % 10 == 0:
                        f_error = open(pickle_error_data, "wb")
                        pickle.dump(total_error_list, f_error)
                        f_error.close()


def analysis_website(driver):
    total_url_list = []

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
        elem_login = driver.find_element_by_name("submit")
        elem_login.click()

    if os.path.exists(pickle_url_data):
        f_data_pickle = open(pickle_url_data, "rb")
        total_url_list = pickle.load(f_data_pickle)
        f_data_pickle.close()


    driver.set_script_timeout(5)
    driver.set_page_load_timeout(5)
    for page_index in range(max_nocode_count):
        url = base_no_code_url + str(page_index)
        try:
            driver.get(url)
        except:
            print("Execution time exceeded!")
        #time.sleep(2)
        page_list_content = bs.BeautifulSoup(driver.page_source).findAll("h3")
        for title_item in page_list_content:
            try:
                link = title_item.findAll("a")[0]
                title = link.text
                item_link = base_url + "/" + link['href']
                if [item_link, title] in total_url_list:
                    print("{} has already exists".format(item_link))
                    continue
                print(title)
                print(item_link)

                total_url_list.append([item_link, title])
                if len(total_url_list) % 10 == 0:
                    f_pickle = open(pickle_url_data, "wb")
                    pickle.dump(total_url_list, f_pickle)
                    f_pickle.close()

            except:
                print("{} has some error in it!".format(item_link))


'''
web_driver = webdriver.Firefox()
analysis_website(web_driver)
#get_torrent_link(web_driver)
web_driver.quit()
'''
