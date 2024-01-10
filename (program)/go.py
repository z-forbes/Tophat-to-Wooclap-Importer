from main import Main
import utils
import os
import csv
from time import sleep
import re

# checks if questions missing in output
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
        utils.instruction("There are {} questions in input and {} accross outputs.\nThis is likely because of Top Hat question types which Wooclap can't...\n...convert (learningtool and clickontargetquestion) for example. ".format(lines_in-1, lines_out-1))
        input("Press enter to continue.")

# removes/fixes html tags from all output files after they've been created
def fix_tags(out_dir="output/"):
    # replaces provided range in old_str with sub
    def sub_range(old_str, sub_str, start, end):
        if end<start or start<0 or end>len(old_str):
            raise Exception("utils.sub_range() not being used as intended.") 
        start_str = old_str[0:start]
        end_str = old_str[end:]
        return start_str + sub_str + end_str
    
    fpaths = [os.path.join(out_dir, f) for f in os.listdir(out_dir)]
    for fpath in fpaths:
        f = open(fpath, "r")
        output_lines = []
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            new_line = []
            for e in line:
                maths = re.search("<.*>", e)
                if not maths:
                    new_line.append(e)
                    continue
                
                maths_str = maths.group(0)
                maths_str = maths_str.replace("<sup>", "^{").replace("</sup>", "}")
                maths_str = maths_str.replace("<sub>", "_{").replace("</sub>", "}")
                maths_str = maths_str.replace("<strong>", "\\textbf{").replace("</strong>", "}")
                maths_str = maths_str.replace("<br>", "\n")

                if re.findall("<.*?>", maths_str) != []:
                    print(fpath, re.findall("<.*?>", maths_str))
                    maths_str = re.sub("<.*?>", "", maths_str) # try remove all remaining tags
                
                maths_str = f"${maths_str}$"

                e = sub_range(e, maths_str, maths.start(), maths.end())
                new_line.append(e)
            output_lines.append(new_line)

        f.close()
        utils.write_csv(output_lines, fpath)

try:
    os.system('cls')
    f = open("logo.txt", "r")
    print(f.read(), end="\n\n")
    f.close()
    Main(auto=False).main()
    validate()
    fix_tags()
    utils.instruction("Finished")
    os.startfile("img_tol_miss.csv")
    input("Press enter to exit.")
except Exception as e:
    if type(e)==PermissionError:
        utils.exception("Close the file mentioned in the following error message:\n"+str(e))
    if type(e)!=AssertionError:
        print("The program crashed unexpectedly with the following error message...")
        utils.exception(e)
