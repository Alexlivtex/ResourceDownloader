import os
import pickle

pickle_data = os.path.join("file_config", "bt_download", "data_total.pickle")
pickle_data_bak = os.path.join("file_config", "bt_download", "data_total_bak.pickle")

def check_data():
    total_dic_map = {}
    error_list = []
    if os.path.exists(pickle_data):
        try:
            f_data_pickle = open(pickle_data, "rb")
            total_dic_map = pickle.load(f_data_pickle)
            f_data_pickle.close()
        except:
            f_data_pickle = open(pickle_data_bak, "rb")
            total_dic_map = pickle.load(f_data_pickle)
            f_data_pickle.close()
    else:
        print("{} not exists!".format(pickle_data))
        return

    error_count = 0
    for map_index in total_dic_map:
        torrent_link = total_dic_map[map_index][1]
        if len(torrent_link.split(":")) != 4 or len(torrent_link.split("=")) != 2 or len(torrent_link.split(":")[-1]) != 40:
            print(torrent_link)
            error_count+=1
            error_list.append(map_index)

    for error_index in error_list:
        total_dic_map.pop(error_index)

    f_data_pickle = open(pickle_data, "wb")
    pickle.dump(total_dic_map, f_data_pickle)
    f_data_pickle.close()

    print(len(total_dic_map))
