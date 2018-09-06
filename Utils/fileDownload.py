import os
import requests

def download_file(file_url, file_path):
    target_file = os.path.join(file_path, file_url.split("/")[-1])
    if os.path.exists(target_file):
        needRedownload = True if input("Need to download and overwrite?").lower() == "y" else False
        if needRedownload:
            os.remove(target_file)
        else:
            print("No need to download again , just return!")
            return

    r = requests.get(file_url, stream=True)
    with open(target_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)