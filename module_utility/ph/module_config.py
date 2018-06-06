import os
import json

def load_config(config_path, data_path):
    with open(config_path, "r") as f:
        data = json.load(f)

    if data["ph"]["url"] == "":
        data["ph"]["url"] = input("Please input the url address : ")

    if data["ph"]["data_name"] == "ph.pickle":
        data["ph"]["data_name"] = os.path.join(data_path, data["ph"]["data_name"])

    if data["ph"]["data_bak_name"] == "ph_bak.pickle":
        data["ph"]["data_bak_name"] = os.path.join(data_path, data["ph"]["data_bak_name"])

    if data["ph"]["data_error_name"] == "ph_error.pickle":
        data["ph"]["data_error_name"] = os.path.join(data_path, data["ph"]["data_error_name"])

    paramList = data["ph"]
    with open(config_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    return paramList