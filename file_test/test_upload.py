from subprocess import call
import pickle
import os

def pre_check_net_disk():
    total_list = []
    #call(["bypy", "list", "learning_markets_video", " > ", "net_result"])
    os.system("bypy list learning_markets_video > net_result")
    f_net = open("net_result", "r")
    test_lines = f_net.readlines()
    test_lines = test_lines[1:-1]
    f_net.close()
    os.remove("net_result")

    for line_index in test_lines:
        print(line_index.split(" ")[1])
        total_list.append(line_index.split(" ")[1])

    f_net_pickle = open("net_map.pickle", "wb")
    pickle.dump(total_list, f_net_pickle)
    f_net_pickle.close()


pre_check_net_disk()