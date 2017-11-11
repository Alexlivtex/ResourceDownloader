import pickle
import os
from ..timeout.timeout import timeout

def pre_check_net_disk():
    total_list = []
    #call(["bypy", "list", "learning_markets_video", " > ", "net_result"])
    while True:
        try:
            @timeout(15)
            def bypy_list():
                os.system("bypy list learning_markets_video > net_result")
                return
            bypy_list()
            break
        except:
            continue

    f_net = open("net_result", "r")
    test_lines = f_net.readlines()
    test_lines = test_lines[1:-1]
    f_net.close()
    os.remove("net_result")

    for line_index in test_lines:
        print(line_index.split(" ")[1])
        total_list.append(line_index.split(" ")[1])

    f_net_pickle = open(os.path.join("file_config", "learning_markets", "learning_markets_net_map.pickle"), "wb")
    pickle.dump(total_list, f_net_pickle)
    f_net_pickle.close()