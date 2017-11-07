import os
import pickle
import libtorrent as lt
import time
import sys

from module_utility.bt_download.check_disk_status import check_disk_percentage

torrent_dir_name = os.path.join("file_local", "bt_download", "torrent_dir")
bt_download_dir = os.path.join("file_download","bt_download", "download_dir")

finished_downloading_list = []
finished_downloading_data = os.path.join("file_config", "bt_download", "finished_downloading.pickle")

current_downloading_data = os.path.join("file_config", "bt_download", "current_downloading.pickle")

failed_download_list = []
failed_downloading_data = os.path.join("file_config", "bt_download", "failed_downloading.pickle")

def download_torrent(torrent_file):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    download_time = 0

    e = lt.bdecode(open(torrent_file, "rb").read())
    info = lt.torrent_info(e)

    print(info)

    params = {'save_path' : bt_download_dir, 'storage_mode': lt.storage_mode_t.storage_mode_sparse, 'ti': info}
    h = ses.add_torrent(params)
    ses.start_dht()

    print 'starting', h.name()

    s = h.status()

    #print s.total_wanted
    percent = check_disk_percentage(float(s.total_wanted)/float(1024))
    print(percent)

    while(not s.is_seeding):
        s = h.status()
        state_str = ['queued', 'checking', 'downloading metadata','downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s\n' % \
          (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
          s.num_peers, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)
        download_time += 1
        if download_time > 18000:
            print("{} has spent too much time to download, quit it!".format(torrent_file))
            f = open(failed_downloading_data, "wb")
            failed_download = pickle.load(f)
            failed_download.append(torrent_file)
            pickle.dump(failed_download, f)
            f.close()
            return
    print h.name(), 'complete'




def begin_download():
    global finished_downloading_list
    global failed_download_list

    if os.path.exists(finished_downloading_data):
        f = open(finished_downloading_data, "rb")
        finished_downloading_list = pickle.load(f)
        f.close()

    if os.path.exists(failed_downloading_data):
        f = open(failed_downloading_data)
        failed_download_list = pickle.load(f)
        f.close()

    if os.path.exists(current_downloading_data):
        f = open(current_downloading_data, "rb")
        current_downloading = pickle.load(f)
        f.close()
        download_torrent(os.path.join(torrent_dir_name, current_downloading))
        os.remove(current_downloading_data)
    else:
        for index in os.listdir(torrent_dir_name):
            print(index)
            if index.split(".")[-1] == "torrent" and index not in finished_downloading_list and index not in failed_download_list:
                f = open(current_downloading_data, "wb")
                pickle.dump(index, f)
                f.close()
                download_torrent(os.path.join(torrent_dir_name, index))
                os.remove(current_downloading_data)



begin_download()
