import os
from bypy import ByPy
from ..timeout import timeout

MAX_WAIT_TIME = 15*60

@timeout(MAX_WAIT_TIME)
def post_process():
    bp = ByPy()
    bp.upload("file_download")
    os.system("rm -rf file_download/learning_markets_video/*")