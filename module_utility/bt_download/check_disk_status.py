import os
def check_disk_percentage(file_size):
    disk = os.statvfs("/root")
    percent = float(disk.f_blocks - disk.f_bfree + file_size) / float(disk.f_blocks)
    print("total number of blocks in filesystem: " + str(disk.f_blocks))
    print("total number of free blocks: " + str(disk.f_bfree))
    percent = format(percent, ".4f")
    percent = float(percent)
    return percent
