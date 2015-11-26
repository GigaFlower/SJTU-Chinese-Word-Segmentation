#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Administrator
#
# Created:     23/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def file():
    f=open("SogouPart.txt","r")
    return f

def database(f):
    s=f.read()
    l=s.split()
    return l

def divide(s):
    length=len(s)
    c=-1
    l=[]
    for m in s:
        if ord(m[0]) >= 128:
            c += 1
            l += [[]]
        l[c].append(m)
    return l

def relist(l):
    wd=[x[0] for x in l]
    pb=[x[1] for x in l]
    return (wd,pb)

def SumAll(l):
    n=0
    for x in l:
        n += int(x)
    return n

def main():
    f=file()
    x=database(f)
    l=divide(x)  # "word"=l[0]; "prob"=l[1]; "lexical"=l[2:]
    wd,pb=relist(l)
    n=SumAll(pb)
    f.close()
    return n

if __name__ == '__main__':
    main()