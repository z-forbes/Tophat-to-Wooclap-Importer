from Processor import Processor
from Tophat import Tophat
import subprocess
import os
import csv
from utils import exception
import utils

class Main:
    def __init__(self, auto):
        self.last_good_line = None
        self.auto = auto
        self.th_dir = "th_to_wc/input/"
        self.wc_dir = "th_to_wc/output/"
        
    # checks for duplicate tags    
    def verify_tags(self):
        tags = []
        th_fpath = self.th_dir+utils.dir_fnames(self.th_dir)[0]
        f = open(th_fpath, "r")
        first = True
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first:
                first = False
                continue
            if len(line)<3:
                continue
            tags.append(utils.get_tag(line[2]))
        f.close()
        tags_count = {t:tags.count(t) for t in tags}
        problem = ""
        for t, c in tags_count.items():
            if t==None:
                ok_lol = "questions are"
                if c==1:
                    ok_lol = "question is"
                if c*2==len(tags):
                    utils.warning("Exactly half of all questions are untagged.", colour=False)
                utils.warning("For your information, {} {} untagged. There are {} questions total.".format(c, ok_lol, len(tags)), colour=False)
                continue
            if c!=1:
                problem+="The tag {} is not unique. It appears {} times.\n".format(t, c)
        if problem !="":
            os.startfile(th_fpath.replace("/", "\\"))
            utils.exception(problem+"You must remove duplicate tags to continue.\nEither choose a unique tag, or remove tag completely.", colour=False)
                




    # removes the first column of a Top Hat extract where neccessary. removes leading encoding chars
    def parse_th(self):
        for fname in utils.dir_fnames(self.th_dir): # shouldn't be a for loop - assured only one file.
            if fname.split(".")[-1]!="csv":
                exception("Format of input file must be csv")
            f = open(self.th_dir+fname, "r")
            output = []
            first = True
            rm_fst_col = False
            l = 0
            for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
                l+=1
                self.last_good_line = l
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

                line[3] = line[3].replace("\n<br>", "") # tag not removed by Wooclap's code
                line[3] = line[3].replace("<br>", "") # cba using regex
                output.append(line)
            f.close()

            if output!=[]:
                utils.write_csv(output, self.th_dir+fname)


    def main(self):
        fnames = utils.dir_fnames(self.th_dir)
        if len(fnames)!=1:
            utils.exception("{} input files provided. Exactly 1 is required.".format(len(fnames)), colour=False)

        try:
            self.parse_th()
        except UnicodeError as e:
            utils.exception("There is an invalid character in line {} of your input file. Try rewriting this line or using a different encoding.\n{}".format(self.last_good_line+1, e), colour=False)
        self.verify_tags()

        if not os.path.exists('th_to_wc/node_modules'):
            subprocess.call(['get_modules.bat'])
        subprocess.call(['run.bat'])

        p = Processor(wc_dir=self.wc_dir, auto=self.auto)
        p.run()

        th = Tophat(self.th_dir, show_warnings=(not self.auto))
        th.mk_img_tol_miss(p)

        os.remove("joined_input.csv")

        return p