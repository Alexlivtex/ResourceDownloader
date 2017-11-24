import pyminizip
import os
compression_level = 5
import shutil

def walk_file_path(path):
    file_list = []
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            f.encode('UTF-8')
            file_list.append(os.path.join(fpathe, f))
            print os.path.join(fpathe, f)

    return file_list

def compress_folder(folder_name, dst_path):
    file_list = walk_file_path(folder_name)
    pyminizip.compress_multiple(file_list, dst_path, "133456", compression_level)
    shutil.rmtree(folder_name)

