#-------------------------------------------------------------------------------
# Name:        妯″潡1
# Purpose:
#
# Author:      Administrator
#
# Created:     18/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def file_sg():
    f=open("SogouPart.txt","r")
    return f

def file_baidu():
    f=open("Baidu_wordlist.txt","r")
    return f

def RemPunc(x):
    s=""
    for c in x:
        if c == ",":
            s += " "
        else:
            s += c
    return s

def divide(x):
    s=x.split()
    c=-1
    l=[]
    for m in s:
        if ord(m[0]) >= 128:
            c += 1
            l += [[]]
        l[c].append(m)
    return l

def CreateDic(l):
    key=[]
    prob=[]
    for m in l:
        key.append(m[0])
        prob.append(m[1])
    dic=dict(zip(key,prob))
    return dic

def SogouDatabase():
    f_sg=file_sg().read()
    f=RemPunc(f_sg)
    l=divide(f)
    dic=CreateDic(l)
    file_sg().close()
    return (dic,l)

def FourWordsKeep(x,dic):
    l=[]
    for m in x:
        if len(m[0]) == 4 and m[0] not in dic:
            l.append(m)
    return l

def AddIdiom(x):
    for i in range(len(x)):
        x[i].append("TERM")
    return x

def BaiduDatabase(dic):
    f_bd=file_baidu().read()
    l=divide(f_bd)
    l2=FourWordsKeep(l,dic)
    l3=AddIdiom(l2)
    file_baidu().close()
    return l3

def Join(l):
    line=[]
    for m in l:
        m[1]=str(m[1])
        ms=" ".join(m)
        line.append(ms)
    s=" ".join(line)
    return s

def rewrite(s):
    FileName="upgrade_wordlist.txt"
    f=open(FileName,"w")
    f.write(s)
    f.close()

def main():
    dic=SogouDatabase()[0]
    l_sg=SogouDatabase()[1]
    l_bd=BaiduDatabase(dic)
    l=l_sg+l_bd
    s=Join(l)
    rewrite(s)

main()