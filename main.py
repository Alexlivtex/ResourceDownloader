import json
import os
import getpass
from DBHelper import dbConnect
from Utils import webOperation

def main():
    data = {}
    if os.path.exists("config.json"):
        needModify = input("Need to modify the database information? Y/N : ")
        if str(needModify).lower() == "y":
            os.remove("config.json")
        elif str(needModify).lower() == "n":
            print("Just keep the current configuation!")
        else:
            print("Invalid input, please re-input the config information!")
            os.remove("config.json")

    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            data = json.load(f)
            host = data["host"]
            port = data["port"]
            user = data["user"]
            password = getpass.getpass("Please input the password of the user {} : ".format(user))
    else:
        host = input("Please input the host address : ")
        port = input("Please input the database port : ")
        user = input("Please input the user name of the database : ")
        password = getpass.getpass("Please input the password of the database : ")
        data["host"] = host
        data["port"] = port
        data["user"] = user
        with open("config.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    db = dbConnect.connect(host, int(port), user, password)
    db = dbConnect.check_database(host, int(port), user, password, db)
    dbConnect.check_table(db)

    webHandle = webOperation.openBrowser()

main()
