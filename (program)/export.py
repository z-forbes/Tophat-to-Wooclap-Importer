from os import remove, listdir
from shutil import rmtree
import utils
try:
    rmtree("th_to_wc/node_modules")
except:
    utils.warning("node modules already deleted")

try:
    io_dirs = ["th_to_wc/input/", "th_to_wc/output/"]
    for io in io_dirs:
        for f in listdir(io):
            remove(io+f)
except:
    utils.warning("to_to_wc io files already deleted")

try:
    out_dir = "output/"
    for f in listdir(out_dir):
        remove(out_dir+f)
except:
    utils.warning("output files already deleted")

try:
    remove("img_tol_miss.csv")
except:
    utils.warning("img_tol_mis already deleted")

try:
    remove("data_import.csv")
except:
    utils.warning("data_import already deleted")

try:
    rmtree("__pycache__")
except:
    utils.warning("__pycache__ already deleted")

input("Export complete.\nPress enter to exit.")