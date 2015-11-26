#-------------------------------------------------------------------------------
# Name:        婵☆垪鈧櫕鍋?
# Purpose:
#
# Author:      Administrator
#
# Created:     16/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import database

dic,lex_dic=database.main()

def Input():
    x=input("Please enter a sentence in Chinese.")
    return x

def cut(subx,x):
    c=x[len(subx):]
    return c

def match(length,x,DivList=[]):
    global dic
    for i in range(length,3,-1): # Search whether there are four-character words.
        subx=x[:i]
        if subx in dic:
            x=cut(subx,x)
            DivList.append(subx)
            return x,DivList
    return x[1:],DivList

def divide(x):
    global dic
    DivList=[]
    while x != "":
        length=len(x)
        if length < 10: # The longest word in the wordlist has 10 characters.
            x,DivList=match(length,x,DivList)
        else:
            x,DivList=match(10,x,DivList)
    return DivList

def JoinDiv(x):
    s="/".join(x)
    return s

def main():
    x=Input()
    DivList=divide(x)
    s=JoinDiv(DivList)
    print(s)

if __name__ == '__main__':
    main()
