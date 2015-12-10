#-------------------------------------------------------------------------------
# Name:        濠碘槅鍨埀顒冩珪閸?
# Purpose:
#
# Author:      Administrator
#
# Created:     07/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import database , dts_calculate , mi,judge

dic_pb , dic_cha , dic_pro = database.database_main()

def original_file():
    f = open("original_file_wd.txt","r",encoding="utf-16")
    return f

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

def set_judge_property(dts_mean,dts_st_der,string_dts_list,mi_mean,mi_st_der,string_mi_list):
    j = judge.judge()
    j.dts_mean = dts_mean
    j.dts_standard_derivation = dts_st_der
    j.dts_list = [x[1] for x in string_dts_list]
    j.mi_mean = mi_mean
    j.mi_standard_derivation = mi_st_der
    mi_list = [x[1] for x in string_mi_list]
    j.mi_list = mi_list[1:-1]
    return j

def slice(mark_list,string):
    r_string = string[1:-1]
    length = len(r_string)
    subs = r_string[0]
    for num in range(length-1):
        if mark_list[num] == "separated":
            add = "/" + r_string[num + 1]
            subs += add
        else:
            subs += r_string[num + 1]
    return subs

def main():
    file = original_file()
    x = file.read()
    string , method = term_segmentation(x)
    dts = dts_calculate.dts()
    dts_mean , dts_standard_derivation , string_with_dtscore_list = dts.dts_calculate_main(string)
    m = mi.mi()
    mi_mean , mi_standard_derivation , string_with_mi_list = m.mi_main(string)
    j = set_judge_property(dts_mean,dts_standard_derivation,string_with_dtscore_list , mi_mean,mi_standard_derivation , string_with_mi_list)
    mark_list = j.main()
    subs = slice(mark_list , string)
    print(subs)
    file.close()

if __name__ == '__main__':
    main()
