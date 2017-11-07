import os
MAX_DISK_SPACE = 20*1024*1024*1024

def check_max_acceptable_size():
    disk = os.statvfs("/root")
    percent = float(disk.f_blocks - disk.f_bfree) / float(disk.f_blocks)
    print("total number of blocks in filesystem: " + str(disk.f_blocks))
    print("total number of free blocks: " + str(disk.f_bfree))
    percent = format(percent, ".4f")
    percent = float(percent)

    max_file_size = ((1.0 - percent)*MAX_DISK_SPACE*0.7) / 2.0
    return max_file_size
