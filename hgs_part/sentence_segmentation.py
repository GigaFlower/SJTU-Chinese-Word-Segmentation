#-------------------------------------------------------------------------------
# Name:        婵☆垪鈧櫕鍋?
# Purpose:
#
# Author:      Administrator
#
# Created:     03/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


def origin_file():
    f = open("original_file.txt","r",encoding="gb2312")
    return f

def punctuation_standard_file():
    f = open("punctuation_standard_file.txt","r",encoding="gb2312")
    return f

def cut(s,punc_stan):
    '''
    We will cut the whole string into several sentences according to the sentence segment punctuations.
    The punctuations are reserved, but there exists a special case that "\n" should be deleted.
    The completed sentences will be put in the list "s_complete".
    '''
    subs = ""
    s_complete = []
    for cha in s:
        if cha == "\n":
            s_complete.append(subs)  # The linebreak "\n" is not included.
            subs = ""
        else:
            subs = "".join((subs,cha))
            if cha in punc_stan:
                s_complete.append(subs)  # If the sentence segment punctuations("\n" is excluded) are detected, the sentence should be cutted here.
                subs = ""
            else:
                pass
    return s_complete

def main():
    or_f = origin_file()
    whole_string = or_f.read()
    punc_standard = punctuation_standard_file().read()  # "punc_standard" are sentence segment punctuations.
    string_cutted = cut(whole_string,punc_standard)
    or_f.close()
    punctuation_standard_file().close()
    print(string_cutted)

if __name__ == '__main__':
    main()
