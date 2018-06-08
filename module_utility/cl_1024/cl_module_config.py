import json

def load_config(config_path,data_path):
    with open(config_path, "r") as f:
        data = json.load(f)
        if  data["cl1024"]["url"] == "":
            print("Please input the address:")
            data["cl1024"]["url"] = input()
        if data["cl1024"]["id"] == "":
            print("Please input the id:")
            data["cl1024"]["id"] = input()
        if data["cl1024"]["password"] == "":
            print("Please input the password: ")
            data["cl1024"]["password"] = input()

        data["cl1024"]["data_path"] = data_path

    param_list = data["cl1024"]

    with open(config_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    return param_list
