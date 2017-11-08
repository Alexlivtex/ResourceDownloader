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

tmp_dir_name = os.path.join("file_local", "bt_download", "torrent_dir")
pickle_data = os.path.join("file_config", "bt_download", "data_total.pickle")

finished_transform_list = []
finished_transform_data = os.path.join("file_config", "bt_download", "finished_transform.pickle")



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


def torrent_transform():
    global finished_transform_list
    total_list = {}

    if os.path.exists(pickle_data):
        f_pickle = open(pickle_data, "rb")
        total_list = pickle.load(f_pickle)
        f_pickle.close()

    if os.path.exists(finished_transform_data):
        f = open(finished_transform_data, "rb")
        finished_transform_list = pickle.load(f)
        f.close()

    for link_index in total_list:
        if total_list[link_index][1][:6] == "magnet":
            link = total_list[link_index][1]
            if link in finished_transform_list and os.path.exists(os.path.join(tmp_dir_name, link.split(":")[-1] + ".torrent")):
                print("{} has already finished transforming".format(link))
                continue
            else:
                print("Begin to transform {}".format(link))
                try:
                    magnet2torrent(link)
                except:
                    continue


torrent_transform()
