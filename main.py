import json
import os
from DBHelper import dbConnect

def main():
    data = {}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            data = json.load(f)
            host = data["host"]
            port = data["port"]
            user = data["user"]
            password = data["password"]
    else:
        host = input("Please input the host address :")
        port = input("Please input the database port :")
        user = input("Please input the user name of the database :")
        password = input("Please input the password of the database :")
        data["host"] = host
        data["port"] = port
        data["user"] = user
        data["password"] = password
        with open("config.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    db = dbConnect.connect(host, int(port), user, password)
    dbConnect.check_database(db)
    dbConnect.check_table(db)

main()