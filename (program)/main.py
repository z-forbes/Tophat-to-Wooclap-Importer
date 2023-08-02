from Processor import Processor
from Tophat import Tophat
import subprocess
import os
import csv
from utils import exception
import utils

# removes the first column of a Top Hat extract where neccessary. removes leading encoding chars
def parse_th():
    th_dir = "th_to_wc/input/"
    for fname in utils.dir_fnames(th_dir):
        if fname.split(".")[-1]!="csv":
            exception("Format of input file must be csv")
        f = open(th_dir+fname, "r")
        output = []
        first = True
        rm_fst_col = False
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first:
                first = False
                if len(line)==0:
                    exception("First line of input is blank.")
                course_id = "course_id"
                item_id = "item_id"

                if not line[0] in [course_id, item_id]:    
                    try:
                        line[0] = line[0][3:]
                        if not line[0] in [course_id, item_id]:
                            raise Exception()
                    except:
                        exception("File in the wrong format.\nHeaders are: {}".format(line))
                # headers now well-formatted
                if course_id in line:
                    if not item_id in line:
                        exception("Headers do not contain course of item id: {}".format(line))
                    rm_fst_col = True    
            
            if rm_fst_col:
                line = line[1:]
            output.append(line)
        f.close()

        if output!=[]:
            utils.write_csv(output, th_dir+fname)


    



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