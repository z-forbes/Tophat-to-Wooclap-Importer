from main import main
from os import remove, startfile
import utils

try:
    import_path = "data_import.csv"
    f = open(import_path, "a")
    f.close()
    reset = "r"
    user_in = input("Enter {} to reset and open {}. Enter anything else to open it.".format(reset, import_path))
    if user_in==reset:
        remove(import_path)
        p = main(True)
        p.mk_template()
        p.reset_output()
    startfile(import_path)
except Exception as e:
    utils.exception(e)