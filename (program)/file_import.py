from main import Main
from os import remove, startfile, system
import utils
from utils import my_input

try:
    system('cls')
    import_path = "data_import.csv"
    f = open(import_path, "a")
    f.close()
    reset = "t"
    nothing = "o"
    user_in = my_input("Opening {} to allow folder to be named from file.\n\nEnter:\n[{}] to reset the file, make template, and open.\n[{}] to open the file without changing it.\n".format(import_path, reset, nothing))
    while True:
        user_in = user_in.lower()
        if user_in==reset:
            remove(import_path)
            p = Main(auto=True).main()
            p.mk_template()
            p.reset_output()
            break
        if user_in==nothing:
            break
        user_in = my_input("Invalid input. Enter {} or {}.".format(reset, nothing))
    
    startfile(import_path)
except Exception as e:
    if type(e)==PermissionError:
        utils.exception(e, colour=False)
    if type(e)!=AssertionError:
        print("The program crashed unexpectedly with the following error message...")
        utils.exception(e, colour=False)