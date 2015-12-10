# -------------------------------------------------------------------------------
# Name:        Administrator
# Purpose:
#
# Author:      Administrator
#
# Created:     03/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------


def get_origin_file():
    f = open("original_file.txt","r",encoding = "utf-16")
    return f

def get_punctuation_standard_file():
    f = open("punctuation_standard_file.txt","r",encoding = "utf-16")
    return f

def cut(string,punc_stan):
    '''
    We will cut the whole string into several sentences according to the sentence segment punctuations.
    The punctuations are reserved, but there exists a special case that "\n" should be deleted.
    The completed sentences will be put in the list "s_complete".
    '''
    substring = ""
    string_complete = []
    for cha in string:
        if cha == "\n":
            string_complete.append(substring)  # The linebreak "\n" is not included.
            substring = ""
        else:
            substring += cha
            if cha in punc_stan:
                string_complete.append(substring)  # If the sentence segment punctuations("\n" is excluded) are detected, the sentence should be cutted here.
                substring = ""
            else:
                pass
    return string_complete

def main():
    or_f = get_origin_file()
    whole_string = or_f.read()
    punc_standard = get_punctuation_standard_file().read()  # "punc_standard" are sentence segment punctuations.
    string_cutted = cut(whole_string,punc_standard)
    or_f.close()
    get_punctuation_standard_file().close()
    return string_cutted

if __name__ == '__main__':
    main()
