#-------------------------------------------------------------------------------
# Name:        濡€虫健1
# Purpose:
#
# Author:      Administrator
#
# Created:     23/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sum_total_prob

def file():
    f=open("Corpus_characterlist.txt","r")
    return f

def divide(s):
    x=s.split()
    length=len(x)
    wd,prob=[],[]
    for i in range(length):
        if i % 2 == 0:
            wd.append(x[i])
        else:
            prob.append(x[i])
    return wd,prob

def SumAll(l):
    n=0
    for x in l:
        n += int(x)
    return n

def ResetProb(OrgnProb,total,ChaTotal):
    NewProb=[]
    for x in OrgnProb:
        x = int(int(x) / ChaTotal * total)
        NewProb.append(x)
    return NewProb

def Join(wd,prob):
    s=""
    for i in range(len(wd)):
        s += wd[i] + " " + str(prob[i]) + " "
    return s

def rewrite(s):
    FileName="character_reset_wordlist.txt"
    f=open(FileName,"w")
    f.write(s)
    f.close()

def main():
    f=file().read()
    wd,prob=divide(f)
    total=sum_total_prob.main()
    ChaTotal=SumAll(prob)
    ResProb=ResetProb(prob,total,ChaTotal)
    s=Join(wd,ResProb)
    rewrite(s)

if __name__ == '__main__':
    main()