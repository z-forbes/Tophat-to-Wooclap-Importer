import re
from os import listdir, remove
from os.path import isfile, join
import csv

### TAGS ###
# returns the tag from a title cell
def get_tag(title):
    tag = re.findall("F[0-9]+(?:S[0-9]+)?Q[0-9]+", title)
    if len(tag)==0:
        # print("No tag found for:", title)
        return None

    assert len(tag)==1
    return tag[0]

# get("F2S4Q1", "S") --> 4
def get_value(tag, t, keys=["F", "S", "Q"]):
    t = t.upper()
    if not t in keys:
        return None
    full = re.findall("{}[0-9]*".format(t), tag)
    if len(full)>1:
        print(full)
    if len(full)==0:
        return None
    assert len(full)==1
    return int(full[0][1:])


# removes a tag from a title cell
def remove_tag(title):
    return re.sub("F[0-9]+(?:S[0-9]+)?Q[0-9]+( \- | )?", "", title)

def pretty_tag(tag):
    return tag.replace("F", "Folder ").replace("S", " Subfolder ").replace("Q", " Question ")

### FILES ###
# returns the first line of a file
def get_csv_headers(fname):
    output = ""
    f = open(fname, "r")
    for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        output = line
        break
    f.close()
    return output

def join_csvs(dirname, outname):
    fnames = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    if len(fnames)==0:
        exception("NO INPUT FILES PROVIDED!!")
    output = []
    first_file = True
    for fname in fnames:
        first_line = True
        f = open(dirname+fname, "r")
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first_line and (not first_file):
                first_line = False
                continue
            output.append(line)
        if first_file:
            first_file = False
        
    with open(outname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(output)
    return outname

def write_csv(contents, fname):
    # punctuation = r"""!"#$%&'()*+,-:;<=>?@\^`{|}~"""
    # if any (p in fname for p in punctuation):
    #     warning("Trying to write a file whose name contains punctuation. May cause unexpected behaviour.")
    with open(fname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(contents)

def dir_fnames(dirname):
    return [f for f in listdir(dirname) if isfile(join(dirname, f))]

# i thought there were going to be more to replace lol
def replace_invalid_chars(string):
    # subs = {old:new}
    subs = {":":"[colon]"}

    for old, new in subs.items():
        string = string.replace(old, new)
    
    return string
    

### MESSAGES ###
def exception(message):
    print('\033[91m' + "\nError: {}\n".format(message) + '\033[0m')
    input("Press enter to exit.")
    raise Exception()

def warning(message):
    print('\033[93m' + "{}".format(message) + '\033[0m')

def instruction(message):
    print('\033[96m' + "{}".format(message) + '\033[0m')
