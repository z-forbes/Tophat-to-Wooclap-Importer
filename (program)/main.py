from Processor import Processor
from Tophat import Tophat
import subprocess
import os
import csv
from utils import dir_fnames, exception

# removes the first column of a Top Hat extract where neccessary
def parse_th():
    th_dir = "th_to_wc/input/"
    for fname in dir_fnames(th_dir):
        if ".xlsx" in fname:
            exception("Must convert excel file to csv.")
        f = open(th_dir+fname, "r")
        output = []
        first = True
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first:
                first = False
                if len(line)==0 or line[0]!="course_id":
                    if line[0]!="item_id":
                        exception("File in the wrong format or wrong encoding used.\nFirst header should not be '{}'.".format(line[0]))
                    break
            output.append(line[1:])
        f.close()

        if output!=[]:
            with open(th_dir+fname, 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(output)

def main(auto):
    parse_th()
    if not os.path.exists('th_to_wc/node_modules'):
        subprocess.call(['get_modules.bat'])
    subprocess.call(['run.bat'])

    p = Processor(wc_dir="th_to_wc/output/", auto=auto)
    p.run()

    th = Tophat("th_to_wc/input/")
    th.mk_img_tol_miss(p)

    os.remove("joined_input.csv")
    return p