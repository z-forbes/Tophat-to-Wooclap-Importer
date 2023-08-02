from main import main
import utils
import os
import csv
from time import sleep

# checks questions missing in output
def validate():
    in_dir = "th_to_wc/input/"
    out_dir = "output/"

    lines_in = 0
    f = open(in_dir+utils.dir_fnames(in_dir)[0], "r")
    for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True): 
        if line[0]=='':
            break
        lines_in +=1
    f.close()

    tmp_fname = "tmp_validation_file.csv"
    utils.join_csvs(out_dir, tmp_fname)
    lines_out = 0
    f = open(tmp_fname, "r")
    for _ in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True): lines_out +=1
    f.close()
    os.remove(tmp_fname)
    if lines_in==lines_out:
        utils.instruction("\nAll {} questions in input are accounted for accross outputs!".format(lines_in-1))
    else:
        utils.exception("There are {} questions in input and {} accross outputs.".format(lines_in-1, lines_out-1))

main(auto=False)
utils.instruction("Finished")
validate()
os.startfile("img_tol_miss.csv")
print("Exiting shortly...")
sleep(3)