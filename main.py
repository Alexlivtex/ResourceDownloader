import json
import os
import sys
import getpass
from DBHelper import dbConnect
from Utils import webOperation
from Utils import cryptography

def main():
    if len(sys.argv) != 2:
        print("Usage : python main.py Run    : Just run the programme directly!")
        print("        python main.py Config : Delete the origin config file and re-config")
        return None

    if str(sys.argv[1]).lower() == "config":
        os.remove("config.json")
        print("Need to re-config the programme")

    data = {}
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


    db = dbConnect.connect(host, int(port), user, password)
    db = dbConnect.check_database(host, int(port), user, password, db, db_name)
    dbConnect.check_table(db)

    webHandle = webOperation.openBrowser()

main()
