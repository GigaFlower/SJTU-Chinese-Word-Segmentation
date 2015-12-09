#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Administrator
#
# Created:     07/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def file():
    f=open("wordlist.txt","r",encoding="utf-16")
    return f

def combine(x):
    s=x.split()
    c=-1
    l=[]
    for m in s:
        if ord(m[0]) >= 128:
            c += 1
            l += [[]]
        l[c].append(m)
    return l

def delete(l):
    f_l=[]
    for m in l:
        if len(m[0]) <= 4:
            f_l.append(m)
    return f_l

def sentence_list(f_l):
    s=[]
    for m in f_l:
        sen=" ".join(m)
        s.append(sen)
    return s

def rewrite(s):
    name="wordlist_final.txt"
    f=open(name,"w")
    f.write(s)
    f.close

def main():
    f=file()
    x=f.read()
    l=combine(x)
    f_l=delete(l)
    s_l=sentence_list(f_l)
    s=" ".join(s_l)
    rewrite(s)

if __name__ == '__main__':
    main()
