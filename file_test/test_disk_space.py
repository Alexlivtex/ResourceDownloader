import os
disk = os.statvfs("/root")
percent = 0.0
percent = float((disk.f_blocks - disk.f_bfree) / disk.f_blocks)
print("total number of blocks in filesystem: " + str(disk.f_blocks))
print("total number of free blocks: " + str(disk.f_bfree))
print("%.5f"%(percent))
