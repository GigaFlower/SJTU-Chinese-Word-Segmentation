#-------------------------------------------------------------------------------
# Name:        濠电姷顣藉Σ鍛村垂椤忓牆鐒垫い鎺戝暞閻濐亪鏌?
# Purpose:
#
# Author:      Administrator
#
# Created:     16/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def file_wd():
    f=open("upgrade_wordlist.txt","r", encoding="gbk")
    return f

def file_cha():
    f=open("Corpus_characterlist.txt","r",encoding="gbk")
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
    lex=[x[2:] for x in l]
    return (wd,pb,lex)

def dictionary(wd,pb):
    dic=dict(zip(wd,pb))
    return dic

def DivideCha(x):
    wd=[]
    prob=[]
    for i in range(len(x)):
        if i % 2 == 0:
            wd.append(x[i])
        else:
            prob.append(x[i])
    return wd,prob

def SolveWd():
    f_wd=file_wd()
    x=database(f_wd)
    l=divide(x)  # "word"=l[0]; "prob"=l[1]; "lexical"=l[2:]
    (wd,pb,lex)=relist(l)
    dic=dictionary(wd,pb)
    lex_dic=dictionary(wd,lex)
    f_wd.close()
    return dic,lex_dic

def SolveCha():
    f_cha=file_cha()
    x=database(f_cha)
    wd,prob=DivideCha(x)
    dic_cha=dictionary(wd,prob)
    f_cha.close()
    return dic_cha

def main():
    dic,lex_dic=SolveWd()
    dic_cha=SolveCha()
    return dic,dic_cha,lex_dic

if __name__ == '__main__':
    main()