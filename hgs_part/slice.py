# -------------------------------------------------------------------------------
# Name:        妯″潡1
# Purpose:
#
# Author:      Administrator
#
# Created:     25/11/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import mi

valve=4  # Set a valve value for slicing.

def Input():
    x=input("Please enter a sentence in Chinese.")
    return x

def combine(x,y):
    global valve
    if x[1] >= valve and y[1] < valve:
        return x[0]
    elif x[1] < valve and y[1] >= valve:
        return y[0]  # "else" case remains to be written.

def FindMi(x,dic):
    global valve
    try:
        n=dic[x]
        return n
    except:
        return -100

def search(s,dic):
    global valve
    x=1
    while x < len(s):
        if dic[s[x-1:x+1]] >= valve:
            s = s[0:x+1] + "/" + s[x+1:]
            x += 3
        else:
            s = s[0:x] + "/" + s[x:]
            x += 2
    return s

def main():
    s=Input()
    dic,l=mi.main(s)
    s=search(s,dic)
    print(l)
    print(s)

if __name__ == '__main__':
    main()
