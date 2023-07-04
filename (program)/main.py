from Processor import Processor
from Tophat import Tophat
import subprocess
import os

def main(auto):
    if not os.path.exists('th_to_wc/node_modules'):
        subprocess.call(['get_modules.bat'])
    subprocess.call(['run.bat'])

    p = Processor(wc_dir="th_to_wc/output/", auto=auto)
    p.run()

    th = Tophat("th_to_wc/input/")
    th.mk_img_tol_miss(p)

    os.remove("joined_input.csv")
    return p