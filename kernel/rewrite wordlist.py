#-------------------------------------------------------------------------------
# Name:        濡€虫健1
# Purpose:
#
# Author:      Administrator
#
# Created:     10/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class rewrite_wordlist:
    def __init__(self):
        pass

    def file_word(self):
        f = open("wordlist_aft_term.txt","r", encoding = "utf-16")
        return f

    def split_into_list(self,f):
        '''
        We split the lexicon into lots of lists.
        '''
        s = f.read()
        l = s.split()
        return l

    def combine(self,l):
        '''
        We combine the elements of the same word into a list in the form of name, probability and properties.
        '''
        c = -1
        wd_l = []
        for m in l:
            if ord(m[0]) >= 128:  # If a Chinese character is detected, it will be appended into a new element, followed by its probability and properties.
                c += 1
                wd_l += [[]]
            wd_l[c].append(m)
        return wd_l

    def add_prob(self,dic,problist):
        for element in problist:
            if len(element[0]) > 2:
                for num in range(len(element[0])-1):
                    c_ele = element[0][num:num + 2]
                    if c_ele in dic:
                        dic[c_ele] += element[1]
                    else:
                        dic[c_ele] = element[1]
        return dic

    def relist(self,l):
        '''
        This function will relist the words' name, probability and properties into three separate lists.
        '''
        wd = [x[0] for x in l]
        pb = [int(x[1]) for x in l]
        return wd,pb

    def dictionary(self,a,b):
        '''
        This function will make a dictionary of the words.
        '''
        dic=dict(zip(a,b))
        return dic

    def examine(self,dic_f):
        l = []
        for element in dic_f:
            if len(element) == 2:
                l.append(element)
                l.append(str(dic_f[element]))
        return l

    def write(self,l_f):
        s = " ".join(l_f)
        name = "wordlist_v2.txt"
        f = open(name,"w",encoding = "utf-16")
        f.write(s)
        f.close()

    def main(self):
        '''
        It's the process of creating a word dictionary.
        '''
        f_wd = self.file_word()
        l = self.split_into_list(f_wd)
        wd_l = self.combine(l)
        wd,pb = self.relist(wd_l)
        dic_pb = self.dictionary(wd,pb)
        wd_rl = zip(wd,pb)
        dic_f = self.add_prob(dic_pb,wd_rl)
        l_f = self.examine(dic_f)
        self.write(l_f)
        f_wd.close()

class rewrite_term_prob:
    def __init__(self):
        pass

    def file(self):
        f=open("wordlist.txt","r",encoding="utf-16")
        return f

    def combine(self,x):
        s=x.split()
        c=-1
        l=[]
        for m in s:
            if ord(m[0]) >= 128:
                c += 1
                l += [[]]
            l[c].append(m)
        return l

    def rewrite_l(self,l):
        for m in l:
            if 3 <= int(m[1]) <= 7:
                n = int(m[1])
                m[1] = str(100000 * (8 ** (7-n)))
        return l

    def sentence_list(self,f_l):
        s=[]
        for m in f_l:
            sen=" ".join(m)
            s.append(sen)
        return s

    def rewrite(self,s):
        name="wordlist_aft_term.txt"
        f=open(name,"w",encoding = "utf-16")
        f.write(s)
        f.close()

    def main(self):
        f=self.file()
        x=f.read()
        l=self.combine(x)
        f_l=self.rewrite_l(l)
        s_l=self.sentence_list(f_l)
        s=" ".join(s_l)
        self.rewrite(s)
        w = rewrite_wordlist()
        w.main()

p = rewrite_term_prob()
p.main()