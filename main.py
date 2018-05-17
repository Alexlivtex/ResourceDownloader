import json
import os

CONFIG_FILE = os.path.join("file_config", "config.json")


def main():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if data["cl1024"][0]["id"] == "":
            print("Please input the id:")
            data["cl1024"][0]["id"] = input()
        if data["cl1024"][0]["password"] == "":
            print("Please input the password: ")
            data["cl1024"][0]["password"] = input()

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

main()