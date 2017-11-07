import pyminizip
import os
compression_level = 5
import shutil

def compress_folder(folder_name, dst_path):
    file_list = []
    for i in os.listdir(folder_name):
        file_list.append(os.path.join(folder_name, i))
    pyminizip.compress_multiple(file_list, os.path.join(dst_path, "test"), "133456", compression_level)
    shutil.rmtree(folder_name)
