import os
from bypy import ByPy

def post_process():
    bp = ByPy()
    bp.upload("file_download")
    os.system("rm -rf file_download/learning_markets_video/*")