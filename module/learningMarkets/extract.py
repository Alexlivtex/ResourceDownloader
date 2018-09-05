from bs4 import BeautifulSoup
import requests
import os
import time

def insert_table(db, data):
    myCursor = db.cursor()
    if data["Table"] == "Accounts_info":
        '''
        InsertSQL = "INSERT INTO {} (Module, Address, UserName, Password) VALUES ('{}', '{}', '{}', '{}' )".format(
                                     data["Table"], str(data["module"]), str(data["address"]), str(data["user_name"]),
                                     str(data["password"]))
        '''
        InsertSQL = "INSERT INTO {} (Module, Address, UserName, Password) VALUES (%s, %s, %s, %s )".format(data["Table"])
        InsertData = (data["module"], data["address"], data["user_name"], data["password"])
    else:
        myCursor.execute("SELECT * FROM {} WHERE Link='{}'".format(data["Table"], data["Link"]))
        if myCursor.fetchone() != None:
            print("Record link {} has already existed!".format(data["Link"]))
            return
        '''
        InsertSQL = "INSERT INTO {} (Title, Description, DataPublished, Link) VALUES ('{}', '{}', '{}', '{}' )".format(
                                     data["Table"], str(data["Title"]), str(data["Description"]), str(data["DataPublished"]),
                                     str(data["Link"]))
        '''
        InsertSQL = "INSERT INTO {} (Title, Description, DataPublished, Link) VALUES (%s, %s, %s, %s )".format(data["Table"])
        InsertData = (data["Title"], data["Description"], data["DataPublished"], data["Link"])

    try:
        myCursor.execute(InsertSQL, InsertData)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

def create_table(db, data):
    myCursor = db.cursor()
    if data["Table"] == "Accounts_info":
        CREATE_SQL = "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ," \
                                      "Module VARCHAR (100) not NULL ," \
                                      "Address VARCHAR (100) NOT NULL ," \
                                      "UserName VARCHAR (100) NOT NULL ," \
                                      "Password VARCHAR(100) NOT  NULL )".format(data["Table"])
    else:
        CREATE_SQL =  "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY ," \
                                      "Title VARCHAR (500) not NULL ," \
                                      "Description VARCHAR (1000) NOT NULL ," \
                                      "DataPublished VARCHAR (100) NOT NULL ," \
                                      "Link VARCHAR(100) NOT  NULL )".format(data["Table"])

    try:
        myCursor.execute(CREATE_SQL)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

def check_table(db, data):
    myCursor = db.cursor()
    ret = myCursor.execute("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(data["Table"]))
    return ret

def check_record(db ,data):
    myCursor = db.cursor()
    myCursor.execute("SELECT * FROM {} WHERE Module='{}'".format(data["Table"], data["module"]))
    data_line = myCursor.fetchone()
    return data_line

def learningMarketsExtract(db, driver):
    data_accounts = dict()
    data_record = dict()

    data_accounts["Table"] = "Accounts_info"
    data_record["Table"] = "LearningMarkets_Data_Record"

    ret = check_table(db, data_accounts)
    if ret == 0:
        create_table(db, data_accounts)

    ret = check_table(db, data_record)
    if ret == 0:
        create_table(db, data_record)

    data_accounts["module"] = "learningMarkets"

    data_line = check_record(db ,data_accounts)
    if data_line == None:
        data_accounts["address"] = input("Please input the learning markets address : ")
        data_accounts["user_name"] = input("Please input the username (If you have no account just input NULL): ")
        data_accounts["password"] = input("Please input the password (If you do not have account just input NULL): ")
        insert_table(db, data_accounts)
    else:
        data_accounts["address"] = data_line[2]
        data_accounts["user_name"] = data_line[3]
        data_accounts["password"] = data_line[4]

    driver.get(data_accounts["address"])
    time.sleep(10)
    button = driver.find_element_by_class_name("gdpr-agreement")
    button.click()
    time.sleep(10)

    buttont_elem = driver.find_element_by_css_selector(".btn.btn-default.dropdown-toggle")
    if buttont_elem:
        buttont_elem.click()

    # subitem = driver.find_element_by_css_selector(".dropdown-menu.pull-right")
    li_list = driver.find_elements_by_css_selector(".dropdown-item.dropdown-item-button")
    for li_item in li_list:
        if li_item.text == "All":
            li_item.click()
            break

    time.sleep(10)

    link_list = BeautifulSoup(driver.page_source, "lxml")

    driver.close()

    for item in link_list.find_all("tr"):
        td_index = item.find_all('td')
        if len(td_index) > 0:
            #print(td_index[0].text)
            #print(td_index[1].text)
            #print(td_index[2].text)
            #print(td_index[3].a["href"])

            soup = BeautifulSoup(requests.get(td_index[3].a["href"]).content, "lxml")
            video_link = soup.find_all("source")[0]["src"].split("?")[0]
            print(video_link)

            data_insert = dict()
            data_insert["Table"] = "LearningMarkets_Data_Record"
            data_insert["Title"] = str((td_index[0].text))
            data_insert["Description"] = str((td_index[1].text)[1:-1]).replace("'", "\"")
            data_insert["DataPublished"] = str(td_index[2].text)
            data_insert["Link"] = str(video_link)

            #print(data_insert)


            #try:

            #except:
            #    print("Record has an error {}".format(data_insert))

            insert_table(db, data_insert)





