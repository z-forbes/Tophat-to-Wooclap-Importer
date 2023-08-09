import csv
from Folder import *
from utils import *
import os

class Processor:
    def __init__(self, wc_dir, auto=False):           
        self.nc_fname = "data_import.csv"
        joined_fname = "joined_input.csv"
        self.fname=join_csvs(wc_dir, joined_fname)
        
        self.auto = auto
        self.out_folder = "output/" # contents deleted in self.run()
        self.lines = []

        # key: question tag, value: line index
        self.tags_rows = {}
        self.mk_tags_rows()

        # question tree
        self.folders = []
        self.mk_folders()

        # key: folder/subfolder tag, value: (f/sf name, f/sf count)
        self.names_counts = {}
        
        self.course_code = ""

    ### NAMER ### 
    def get_names_counts(self, tag):
        def name_unique(name): return not (name in [nc[0] for nc in self.names_counts.values()])
        
        full_name = ""
        count = -1
        if "S" in tag:
            f_tag = "F{}".format(get_value(tag, "F"))
            full_name += self.names_counts[f_tag][0] + " → "
        name = "name_of_{}".format(tag)
        if not self.auto:
            while True:
                name = input("\nName of {}: ".format(pretty_tag(tag)))
                if name_unique(full_name+name): break

                utils.warning("Name not unique.")
            
            extra = ""
            if not "S" in tag:
                extra = ", excluding those within subfolder(s)"
            while True:
                count = input("No. of questions in {}{}: ".format(pretty_tag(tag), extra))
                if count.isdigit(): break

                utils.warning("Enter a number.")
        
        full_name += name
        return (utils.replace_invalid_chars(full_name), int(count))


    ### OUTPUTTER ###
    # calls helper with every group of tags needed to be written to same file
    def run(self):
        if not self.auto:
            self.order()

        if self.is_nc_from_file():
            self.mk_nc_from_file()
        else:
            self.mk_nc_not_from_file()

        self.reset_output()
        self.mk_lines()
        if not self.auto:
            self.course_code = input("Enter the course code (or leave blank to skip): ")
        for f in self.folders:
            if len(f.subfolders)!=0:
                for sf in f.subfolders:
                    self.run_helper([q.tag for q in sf.questions])
            if len(f.questions)!=0:
                self.order()
                self.run_helper([q.tag for q in f.questions])
        # self.lines = []
        self.write_untagged()

    # creates and writes file for given question tags    
    def run_helper(self, tags):
        contents = [get_csv_headers(self.fname)]
        for t in tags:
            current = self.lines[self.tags_rows[t]]
            current[1] = remove_tag(current[1])
            contents.append(current)

        folder_name = re.sub("Q[0-9]*", "", tags[0]) # should be same for all tags[i], i in range
        if not folder_name in self.names_counts.keys():
            try:
                os.startfile("data_import.csv")
            except:
                pass
            utils.exception("The folder {} was found in input but not in provided folder names.".format(folder_name)) 
        fname = self.names_counts[folder_name][0]
        if self.course_code != "":
            fname = "[{}] ".format(self.course_code) + fname

        write_csv(contents, self.out_folder+fname+".csv")

    def write_untagged(self):
        self.mk_lines()
        output = [self.lines[0]]
        untagged = False
        for l in self.lines[1:]:
            if get_tag(l[1])==None:
                untagged=True
                output.append(l)
        if untagged:
            fname = "untagged.csv"
            if self.course_code != "":
                fname = "[{}] {}".format(self.course_code, fname)
            utils.write_csv(output, self.out_folder+"_"+fname)



    ### GENERATORS ###
    def mk_tags_rows(self):
        f = open(self.fname, "r")
        i=0 # indexing from
        self.tags_rows = {}
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            tag = get_tag(line[1])
            if tag==None:
                i+=1
                continue
            self.tags_rows[tag] = i
            i+=1
        f.close()
    
    
    def mk_folders(self):
        for tag, v in self.tags_rows.items():
            q = Question(get_value(tag, "Q"), v, tag)
            f_i = get_value(tag, "F")
            if not self.get_folder_i(f_i):
                new_folder = Folder(f_i, "F{}".format(get_value(tag, "F")))
                self.folders.append(new_folder)
            self.get_folder_i(f_i).add_question(q, sf_i=get_value(tag, "S"))


    def mk_nc_not_from_file(self):
        if len(self.folders)==0:
            print("\nAll questions untagged.")
            return
        utils.instruction("\nEnter (sub)folder names:")
        for f in self.folders:
            self.names_counts[f.tag] = self.get_names_counts(f.tag)
            if len(f.subfolders)!=0:
                for sf in f.subfolders:
                    self.names_counts[sf.tag] = self.get_names_counts(sf.tag)


    def mk_lines(self):
        self.lines = []
        f = open(self.fname, "r")
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            self.lines.append(line)
        f.close()

    

    ### UTILS ###
    # returns folder with specified i, None if it does not exist
    def get_folder_i(self, f_i, sf_i=None):
        for f in self.folders:
            if f.i==f_i:
                if sf_i:
                    return f.get_subfolder(sf_i)
                else:
                    return f
        return None
    
    # returns the question of given tag. s=None where applicable
    # SHOULD BE MERGED WITH METHOD ABOVE, IS THIS EVEN USED??
    def lookup(self, f, s, q):
        return self.get_folder_i(f, s).get_question(q)
    

    def get_all_qs(self):
        self.mk_lines()
        return [l[1] for l in self.lines]
    
    def reset_output(self):
        for f in listdir(self.out_folder):
            remove(self.out_folder+f)


    ### FOLDERS ###
    def order(self):
        def orderer(fs):
            fs.sort(key=lambda f: f.i)
            for f in fs:
                f.questions.sort(key=lambda q:q.i)
        
        for f in self.folders:
            orderer(f.subfolders)
        orderer(self.folders)

    def get_folders(self):
        output = []
        for f in self.folders:
            output.append(f)
            for sf in f.subfolders:
                output.append(sf)
        return output

    ### IMPORT FROM FILE ###
    def is_nc_from_file(self):
        try:
            f = open(self.nc_fname, "r")
            c = len(f.readlines())
            f.close()
            if c==(len(self.get_folders())+1):
                # looks like it's true
                tmp = ""
                while not (tmp in ["y", "n"]):
                    tmp = input("\nGet names/counts from file? (y/n)").lower()
                    if tmp=="y":
                        return True
                    if tmp=="n":
                        return False
                    utils.warning("Invalid input.\n")
            else:
                return False
        except:
            return False



    def mk_template(self):
        def line(tag):
            return "\n{},,".format(tag)
        
        self.order()

        output = "tag,folder_name,q_count"
        for f_sf in self.get_folders():
            output += line(f_sf.tag)
        
        f = open(self.nc_fname, "w")
        f.write(output)
        f.close()


    def mk_nc_from_file(self):
        # assert self.is_nc_from_file()
        utils.instruction("Using data from file.")
        f_tags = [f.tag for f in self.get_folders()]

        f = open(self.nc_fname, "r")
        first = True
        tags = []
        for tnc in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first:
                first = False
                continue
            
            if csv_line_blank(tnc):
                continue

            tags.append(tnc[0])

            if not len(tnc)==3:
                utils.exception("Line {} has {} elements.".format(tnc[0], len(tnc)))
            
            if not (tnc[0] in f_tags):
                if str_blank(tnc[0]):
                    tnc[0] = "[empty tag]"
                
                try:
                    os.startfile("data_import.csv")
                except:
                    pass
                utils.exception("Invalid tag provided: {}".format(tnc[0]))
            
            if not(tnc[2].isdigit()):
                if str_blank(tnc[2]):
                    tnc[2] = "[empty count]"

                try:
                    os.startfile("data_import.csv")
                except:
                    pass
                utils.exception("Invalid count provided: {}".format(tnc[2]))

            if "S" in tnc[0]:
                try:
                    tnc[1] = self.names_counts["F{}".format(utils.get_value(tnc[0], "F"))][0] + " → " + tnc[1]
                except:
                    utils.exception("Subfolder {} named before parent folder.".format(tnc[0]))
            self.names_counts[tnc[0]] = (replace_invalid_chars(tnc[1]), int(tnc[2]))
        
        tags_count = {t:tags.count(t) for t in tags}
        problem = ""
        for t, c in tags_count.items():
            if c!=1:
                problem+="The tag {} is not unique. It appears {} times.\n".format(t, c)
        if problem!= "":
            os.startfile("data_import.csv")
            utils.exception("Fix the following problems with tags from file:\n"+problem)

        f.close()