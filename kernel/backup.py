#-------------------------------------------------------------------------------
# Name:        妯″潡1
# Purpose:
#
# Author:      Administrator
#
# Created:     14/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def term_segmentation(s):
    '''
    Separate the proper nouns which are labeled as "TERM" in the wordlist.
    '''
    global dic_pro
    method = []
    for i in range(7,3,-1):  # Searching from 7 characters to 4.
        length = len(s)
        for j in range(0,length - i + 1):
            try:
                subs = s[j:j+i]
                if dic_pro[subs] == ["TERM"]:
                    l = [s[j:j+i],j]  # The element in the method list consists of "word" and location.
                    method.append(l)
                    blank = " " * i
                    s = blank.join((s[0:j],s[j+i:]))  # The certain word is removed from the original string.
                else:
                    pass
            except:
                pass
    return s,method

    var_xy = (prob_xy - prob_average) ** 2  / (length + 1)  # len(prob_list) = the number of two-long words = len(three_long_word_list) + 1
    var_yz = (prob_yz - prob_average) ** 2  / (length + 1)