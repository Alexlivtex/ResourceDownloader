#!/usr/bin/env python
#encoding=utf8
import os.path as pt
import sys
import libtorrent as lt
from time import sleep
import os
import shutil
import time
import pickle
import threading
import math
from itertools import islice


tmp_dir_name = os.path.join("file_local", "bt_download", "torrent_dir")
pickle_torrent_parse_data = os.path.join("file_config", "bt_download", "data_total_torrent_parse.pickle")

finished_transform_list = []
finished_transform_data = os.path.join("file_config", "bt_download", "finished_transform.pickle")

max_thread_count = 5


def magnet2torrent(magnet, output_name=None):
    global finished_transform_list
    if not pt.exists(tmp_dir_name):
        os.mkdir(tmp_dir_name)

    tempdir = tmp_dir_name
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
    }
    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    waiting_count = 0
    while (not handle.has_metadata()):
        try:
            sleep(1)
            waiting_count += 1
            if waiting_count > 150:
                print("{} can not be downloaded!".format(magnet))
                ses.pause()
                ses.remove_torrent(handle)
                return
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            sys.exit(0)
    ses.pause()
    print("Done")
    print("Spent {} seconds to finish".format(waiting_count))

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    #output = pt.abspath(torinfo.name() + tempdir + ".torrent")
    #output = torinfo.name() + ".torrent"
    output = magnet.split(":")[-1] + ".torrent"
    output = os.path.join(tempdir, output)

    print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    torrent_content = lt.bencode(torfile.generate())
    f.write(torrent_content)
    f.close()

    if magnet not in finished_transform_list:
        finished_transform_list.append(magnet)
        f = open(finished_transform_data, "wb")
        pickle.dump(finished_transform_list, f)
        f.close()

    try:
        shutil.rmtree(os.path.join(tempdir, torinfo.name()))
    except:
        print("No need to delete {}".format(torinfo.name()))
    ses.remove_torrent(handle)
    return output


def torrent_transform(sub_dic):
    for link_index in sub_dic:
        if sub_dic[link_index][1][:6] == "magnet":
            link = sub_dic[link_index][1]
            if os.path.exists(os.path.join(tmp_dir_name, link.split(":")[-1] + ".torrent")):
                print("{} has already finished transforming".format(link))
                continue
            else:
                print("Begin to transform {}".format(link))
                try:
                    magnet2torrent(link)
                except:
                    continue


def dict_chunks(total_dict, sub_count):
    it = iter(total_dict)
    for i in range(0, len(total_dict), sub_count):
        yield {k:total_dict[k] for k in islice(it, sub_count)}

def main():
    total_list = {}
    if os.path.exists(pickle_torrent_parse_data):
        f_pickle = open(pickle_torrent_parse_data, "rb")
        total_list = pickle.load(f_pickle)
        print(len(total_list))
        f_pickle.close()

    file_list = os.listdir(tmp_dir_name)
    print("Before clean the file count is {}".format(len(file_list)))
    for file_index in file_list:
        if os.path.isdir(os.path.join(tmp_dir_name, file_index)):
            shutil.rmtree(os.path.join(tmp_dir_name, file_index))
    print("After clean the file count is {}".format(len(os.listdir(tmp_dir_name))))

    threads = []
    list_sub_dicts = list(dict_chunks(total_list, int(math.ceil(len(total_list) / max_thread_count))))
    for i in range(max_thread_count):
        threads.append(threading.Thread(target=torrent_transform, args=(list_sub_dicts[i] ,)))

    for t in threads:
        t.setDaemon(True)
        time.sleep(2)
        t.start()

    for thread_index in threads:
        thread_index.join()

while True:
    try:
        print("Begin to transform the torrent!")
        main()
    except:
        print("Wait another period of time to keep on!")
        time.sleep(100)
        continue
