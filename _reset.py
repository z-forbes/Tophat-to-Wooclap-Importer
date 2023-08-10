from os import remove
from utils import dir_fnames, my_input
from shutil import rmtree
from time import sleep

reset = "r"
while True:
    user_in = my_input("Enter {} to reset.".format(reset))
    if user_in.lower()==reset:
        break
    else:
        print("Invalid input.")

for fname in ["img_tol_miss.csv", "joined_input.csv", "data_import.csv", "tmp_validation_file.csv"]:
    try:
        remove(fname)
    except:
        print("{} already deleted.".format(fname))

# remove dir and contents
for dirname in ["__pycache__", "th_to_wc/node_modules"]:
    try:
        rmtree(dirname)
    except:
        print("{} already deleted.".format(dirname))

# remove contents, keep empty dir
for dirname in ["output/", "th_to_wc/input/", "th_to_wc/output/"]:
    try:
        for fname in dir_fnames(dirname):
            remove(dirname+fname)
    except:
        print("{}'s contents already deleted.".format(dirname))

print("\nReset complete.\nProgram will close shortly.")
sleep(3)