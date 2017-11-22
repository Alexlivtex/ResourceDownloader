from selenium import webdriver
import time
import bs4 as bs
import pickle
import os

max_nocode_count = 2500

base_no_code_url = "http://t66y.com/thread0806.php?fid=2&search=&page="
login_url = "http://t66y.com/login.php"
base_url = "http://t66y.com"

#pickle_data = os.path.join("file_config", "bt_download", "data_total.pickle")
pickle_url_data = os.path.join("file_config", "bt_download", "data_url_total.pickle")

def analysis_website(driver):
    total_url_list = []
    driver.implicitly_wait(20)
    driver.set_script_timeout(5)
    driver.set_page_load_timeout(5)

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
                if item_link in total_url_list:
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



try:
    web_driver = webdriver.Firefox()
    analysis_website(web_driver)
    web_driver.quit()
except:
    web_driver.quit()

