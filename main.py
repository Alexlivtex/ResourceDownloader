import json
import os
import getpass
import sys
import traceback
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "module")))
sys.path.append(os.path.abspath(os.getcwd()))

from learningMarkets.main import learningMarketsExtract
from cl_bbs.main import extract_cl_bbs_data

from Utils import DBHelper
from Utils import webOperation
from Utils import cryptography


def main():
    data = {}
    webHandle = None
    if os.path.exists("config.json"):
        with open("config.json") as f:
            data = json.load(f)
    else:
        cryptography.genKey(os.path.join("files", "key.pickle"))
        data["host"] = input("Please input the host address : ")
        data["port"] = input("Please input the database port : ")
        data["user"] = input("Please input the user name of the database : ")
        data["db_name"] = input("Please input the database name:")
        data["password"] = cryptography.encryption_str(str(getpass.getpass("Please input the password of the database : ")), os.path.join("files", "key.pickle"))
        with open("config.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    fp = open("config.json")
    data = json.load(fp)
    host = data["host"]
    port = data["port"]
    user = data["user"]
    db_name = data["db_name"]
    password = cryptography.decryption_str(str(data["password"]), os.path.join("files", "key.pickle"))
    print(os.path.abspath(os.path.join(os.getcwd(), "module")))

    db = DBHelper.connect(host, int(port), user, password)
    if db:
        print("Connect database success!")
    else:
        print("Connect database failed!")

    db = DBHelper.check_database(host, int(port), user, password, db, db_name)
    if db:
        print("check database success!")
    else:
        print("check database failed!")

    try:
        webHandle = webOperation.openBrowser()
        #learningMarketsExtract(db, webHandle)
        extract_cl_bbs_data(db, webHandle)
    except Exception as e:
        print(traceback.format_exc())
        db.close()
        webHandle.close()

main()
