#-------------------------------------------------------------------------------
# Name:        妯″潡1
# Purpose:
#
# Author:      Administrator
#
# Created:     07/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


def file_word():
    f = open("wordlist.txt","r", encoding = "utf-16")
    return f

def file_cha():
    f = open("characterlist.txt","r",encoding = "utf-16")
    return f

def split_into_list(f):
    '''
    We split the lexicon into lots of lists.
    '''
    s = f.read()
    l = s.split()
    return l

def combine(l):
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

def relist(l):
    '''
    This function will relist the words' name, probability and properties into three separate lists.
    '''
    wd = [x[0] for x in l]
    pb = [x[1] for x in l]
    pro = [x[2:] for x in l]
    return wd,pb,pro

def combine_cha(l):
    '''
    We combine the elements of the same character into a list in the form of name and probability.
    '''
    wd=[]
    prob=[]
    for i in range(len(l)):
        if i % 2 == 0:
            wd.append(l[i])
        else:
            prob.append(l[i])
    return wd,prob

def dictionary(a,b):
    '''
    This function will make a dictionary of the words.
    '''
    dic=dict(zip(a,b))
    return dic

def solve_word():
    '''
    It's the process of creating a word dictionary.
    '''
    f_wd = file_word()
    l = split_into_list(f_wd)
    wd_l = combine(l)
    wd,pb,pro = relist(wd_l)
    dic_pb = dictionary(wd,pb)
    dic_pro = dictionary(wd,pro)
    f_wd.close()
    return dic_pb,dic_pro

def solve_cha():
    '''
    It's the process of creating a character dictionary.
    '''
    f_cha = file_cha()
    l = split_into_list(f_cha)
    wd,prob = combine_cha(l)
    dic_cha = dictionary(wd,prob)
    f_cha.close()
    return dic_cha

def database_main():
    dic_pb,dic_pro = solve_word()
    dic_cha = solve_cha()
    return dic_pb,dic_cha,dic_pro

if __name__ == '__main__':
    database_main()
