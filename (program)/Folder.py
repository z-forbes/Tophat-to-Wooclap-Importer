import utils

class Folder:
    def __init__(self, i, tag):
        self.questions = []
        self.subfolders = []
        self.i = i
        self.name = ""
        self.tag = tag

    def add_question(self, q, sf_i=None):
        if sf_i!=None:
            self.ensure_subfolder(sf_i)
            self.get_subfolder(sf_i).add_question(q)
        else:
            self.questions.append(q)
        
    
    def get_question(self, i):
        for q in self.questions:
            if q.i==i:
                return q
        raise Exception("question not found")
    
    def ensure_subfolder(self, sf_i):
        if self.get_subfolder(sf_i):
            return
        self.subfolders.append(Folder(sf_i, "F{}S{}".format(self.i, sf_i)))
        

    def get_subfolder(self, sf_i):
        for sf in self.subfolders:
            if sf.i==sf_i:
                return sf
        return None


class Question:
    def __init__(self, i, v, tag):
        self.i = i
        self.v = v
        self.tag=tag