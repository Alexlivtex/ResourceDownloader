import os
import pickle
import libtorrent as lt
import time
import sys
import shutil
from compress_folder import compress_folder
import progressbar
import math

from check_disk_status import check_max_acceptable_size
from ..learning_markets.check_disk_status import check_disk_percentage

torrent_dir_name = os.path.join("file_local", "bt_download", "torrent_dir")
bt_download_dir = os.path.join("file_download","bt_download", "download_dir")

finished_downloading_list = []
finished_downloading_data = os.path.join("file_config", "bt_download", "finished_downloading.pickle")

current_downloading_data = os.path.join("file_config", "bt_download", "current_downloading.pickle")

failed_download_list = []
failed_downloading_data = os.path.join("file_config", "bt_download", "failed_downloading.pickle")

MAX_AMOUNT_TIME = 18000


def download_torrent(torrent_file, torrent_name):
    global finished_downloading_list
    global failed_download_list
    ses = lt.session()
    ses.listen_on(6881, 6891)

    download_time = 0

    e = lt.bdecode(open(torrent_file, "rb").read())
    info = lt.torrent_info(e)

    print(info)

    params = {'save_path' : bt_download_dir, 'storage_mode': lt.storage_mode_t(2), 'ti': info}
    h = ses.add_torrent(params)
    ses.start_dht()

    print 'starting', h.name()
    s = h.status()
    file_size = s.total_wanted
    print(file_size)
    print(check_max_acceptable_size())

    if not os.path.exists(current_downloading_data):
        if file_size > check_max_acceptable_size():
            print("File is too large, exit!")
            return
        else:
            print("File size is OK, can be downloaded!")

    '''
    format_custom_text = progressbar.FormatCustomText(
        "Down : %(down).1f k/s, Up : %(up).1f k/s, Time used : %(used).1f%%, Progress : %(finished).1f%%",
        dict(
            down=0.25,
            up=0.25,
            used=0.25,
            finished=0.25,
        ),
    )
    '''

    #bar = progressbar.ProgressBar(max_value=s.total_wanted, widgets=[format_custom_text, progressbar.Bar()])
    average_speed = float(s.total_wanted)/float(MAX_AMOUNT_TIME)

    while(not s.is_seeding):
        s = h.status()

        state_str = ['queued', 'checking', 'downloading metadata','downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\r%.2f%% complete %d Remain (down: %.1f kb/s up: %.1f kB/s peers: %d) %s\n' % \
          (s.progress * 100, MAX_AMOUNT_TIME - download_time,  s.download_rate / 1000, s.upload_rate / 1000, \
          s.num_peers, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)
        if s.download_rate < average_speed:
            download_time += 1
        else:
            download_time = download_time - math.ceil(float(s.download_rate)/float(average_speed))

        #format_custom_text.update_mapping(down=s.download_rate/1000, up=s.upload_rate/1000, used=(float(download_time)/float(18000))*100, finished=s.progress * 100)
        #bar.update(s.total_wanted_done)

        if download_time > MAX_AMOUNT_TIME:
            if int(s.progress * 100) < 90:
                print("{} has spent too much time to download, quit it!".format(torrent_file))
                f = open(failed_downloading_data, "wb")
                failed_download_list.append(torrent_name)
                pickle.dump(failed_download_list, f)
                f.close()
                shutil.rmtree(os.path.join(bt_download_dir, h.name()))
                return
            else:
                break
    print h.name(), 'complete'
    f = open(finished_downloading_data, "wb")
    finished_downloading_list.append(torrent_name)
    pickle.dump(finished_downloading_list, f)
    f.close()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    timestr = timestr + "-download"
    compress_folder(os.path.join(bt_download_dir, h.name()), os.path.join(bt_download_dir, timestr))

def begin_download():
    global finished_downloading_list
    global failed_download_list

    if os.path.exists(finished_downloading_data):
        f = open(finished_downloading_data, "rb")
        finished_downloading_list = pickle.load(f)
        f.close()
    else:
        f = open(finished_downloading_data, "wb")
        pickle.dump(finished_downloading_list, f)
        f.close()

    if os.path.exists(failed_downloading_data):
        f = open(failed_downloading_data, "rb")
        failed_download_list = pickle.load(f)
        f.close()
    else:
        f = open(failed_downloading_data, "wb")
        pickle.dump(failed_download_list, f)
        f.close()

    max_download_count = 1
    current_downloaded = 0
    for index in os.listdir(torrent_dir_name):
        if current_downloaded >= max_download_count:
            break

        percent = check_disk_percentage()
        if percent > 0.80:
            break

        if os.path.exists(current_downloading_data):
            f = open(current_downloading_data, "rb")
            current_downloading = pickle.load(f)
            f.close()
            download_torrent(os.path.join(torrent_dir_name, current_downloading), current_downloading)
            os.remove(current_downloading_data)
            current_downloaded += 1
            continue
        else:
            file_list = os.listdir(bt_download_dir)
            if len(file_list) > 0:
                for file_item in file_list:
                    if os.path.isdir(os.path.join(bt_download_dir, file_item)):
                        shutil.rmtree(os.path.join(bt_download_dir, file_item))
                break
            print(index)
            if index.split(".")[-1] == "torrent" and index not in finished_downloading_list and index not in failed_download_list:
                f = open(current_downloading_data, "wb")
                pickle.dump(index, f)
                f.close()
                download_torrent(os.path.join(torrent_dir_name, index), index)
                os.remove(current_downloading_data)
                current_downloaded += 1
            continue
#begin_download()
