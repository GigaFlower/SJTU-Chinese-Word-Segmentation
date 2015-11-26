#-------------------------------------------------------------------------------
# Name:        妯″潡1
# Purpose:
#
# Author:      Administrator
#
# Created:     25/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import database,math

dic,dic_cha,lex_dic=database.main()

def divide(s):
    subs=[]
    for i in range(len(s)-1):
        subs.append(s[i:i+2])
    return subs

def SearchProb(x):
    global dic,dic_cha
    if len(x) == 1:
        try:
            p=dic_cha[x]
            return int(p)
        except:
            return 5
    else:
        try:
            p=dic[x]
            return int(p)
        except:
            return 5

def CalculateMi(xy):
    x=xy[0]
    y=xy[1]
    Pxy=SearchProb(xy)
    Px=SearchProb(x)
    Py=SearchProb(y)
    mi=math.log2( Pxy * 1000 / ( Px * Py ))
    return mi

def JudgeMi(ListS):
    mi=[]
    for i in range(len(ListS)):
        n=CalculateMi(ListS[i])
        mi.append(n)
    return mi

def remix(ListS,mi):
    dic=dict(zip(ListS,mi))
    l=list(zip(ListS,mi))
    return dic,l

def main(s):
    ListS=divide(s)
    mi=JudgeMi(ListS)
    dic,l=remix(ListS,mi)
    return dic,l

if __name__ == '__main__':
    main(s)
