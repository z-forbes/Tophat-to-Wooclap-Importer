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
    if len(tag)!=1:
        if len(set(tag))==1: # all elements in tag the same
            # warning("Same tag appears multiple times in line: {}".format(title))
            return tag[0]
        else:
            exception("Different tags appear in the same line: {}".format(title))
    return tag[0]

# get("F2S4Q1", "S") --> 4
def get_value(tag, t, keys=["F", "S", "Q"]):
    if tag==None:
        return None
    t = t.upper()
    if not t in keys:
        return None
    full = re.findall("{}[0-9]*".format(t), tag)
    # if len(full)>1:
    #     print(full)
    if len(full)==0:
        return None
    if len(full)!=1:
        exception("Tag ({}) formatted incorrectly".format(tag))
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

# joins content from two csvs. no input validation. assumes they have the same headers, which are preserved.
def join_csvs(dirname, outname):
    fnames = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    if len(fnames)==0:
        exception("No input files provided.")
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
    
    write_csv(output, outname)
    return outname

# contents is 2D array
def write_csv(contents, fname):
    with open(fname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(contents)

# gets all filenames from a directory 
def dir_fnames(dirname):
    return [f for f in listdir(dirname) if isfile(join(dirname, f))]

def replace_invalid_chars(string):
    # subs = {old:new}
    subs = {":":"[colon]"} # i thought there were going to be more then this rip

    for old, new in subs.items():
        string = string.replace(old, new)
    
    return string
    

### MESSAGES ###
# terminates program
def exception(message, colour=True):
    full = "\nError: {}\n".format(message)
    if colour:
        print('\n\033[91m' + full + '\033[0m')
    else:
        print(full)
        
    input("Press enter to exit.")
    raise AssertionError()

def warning(message, colour=True):
    message = str(message)
    if colour:
        print('\033[93m' + message + '\033[0m')
    else:
        print(message)

def instruction(message, colour=True):
    message = str(message)
    if colour:
        print('\033[96m' + message + '\033[0m')
    else:
        print(message)


### OTHER ###
# checks if string is blank
def str_blank(s):
    return s==None or s=="" or s.replace(" ", "")==""

def csv_line_blank(l):
    if l==None or len(l)==0:
        return True 

    return not False in [str_blank(str(e)) for e in l]