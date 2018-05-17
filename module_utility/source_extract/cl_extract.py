import bs4 as bs
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

def extract_source_asis_nocode(driver, url):
    index = 1
    complete_url = url + "/thread0806.php?fid=" + str(section_map["NOCODE_ASIA"]) + "&search=&page=" + str(index)
    print(complete_url)
    driver.get(complete_url)
    soup = bs.BeautifulSoup(driver.page_source, "lxml")
    page_total = soup.findAll("onblur")
    print(page_total)