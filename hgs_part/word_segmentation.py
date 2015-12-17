

import time
import database , dts_calculate , mi,judge , term_segmentation

dic_pb , dic_cha , dic_pro = database.database_main()

"""
"dic_pb" is the dictionary with words and their probabilities.
"dic_cha" is the dictionary with characters and their probabilities.
"dic_pro" is the dictionary with words and their properties.
"""


def set_judge_property(dts_mean,dts_st_der,string_dts_list,mi_mean,mi_st_der,string_mi_list,mark_list):
    """
    This function will be used to set the properties of the class "judge" in
    judge.py.
    """
    j = judge.judge()
    j.dts_mean = dts_mean
    j.dts_standard_derivation = dts_st_der
    j.dts_list = [x[1] for x in string_dts_list]
    # Only sending the dts_list with only numbers to judge.py
    j.mi_mean = mi_mean
    j.mi_standard_derivation = mi_st_der
    mi_list = [x[1] for x in string_mi_list]
    # Only sending the mi_list with only numbers to judge.py
    j.mi_list = mi_list[1:-1]
    j.mark_list = mark_list
    return j

def combine(mark_list,string):
    """
    This function will combine the characters again according to the "mark_list".
    When it comes to "separated", the adjacent characters tend to separate and
    the separate mark will be added.
    In other cases, they tend to be bound.
    """
    length = len(string)
    subs = string[0]
    for num in range(length-1):
        if mark_list[num] == "separated":
            add = "/" + string[num + 1]
            subs += add
        else:
            subs += string[num + 1]
    return subs

def main(x):
    """
    This is the main structure of the word segmentation part.
    First, calculate the mi and the dt-score of each word.
    Then, then all the information will be sent to judge.py and in the file
    judge.py, there are three rounds judging whether the two adjacent characters
    should be bound or separated.
    Finally, the relationships between each two adjacent characters will be sent
    back, and through the "combine" function, the separate characters will be
    combined again with the separate mark "/".
    """
    t = term_segmentation.term_seg()
    string_aft_termseg, mark_list = t.term_segmentation(x)
    string = " " + string_aft_termseg + " "
    # Add " " in front of  the first character and behind the last character,
    # which will be used as an auxiliary in the calculation of mi and dtscore.
    dts = dts_calculate.dts()
    dts_mean , dts_standard_derivation , string_with_dtscore_list = dts.dts_calculate_main(string)
    m = mi.mi()
    mi_mean , mi_standard_derivation , string_with_mi_list = m.mi_main(string)
    j = set_judge_property(dts_mean,dts_standard_derivation,string_with_dtscore_list , mi_mean,mi_standard_derivation , string_with_mi_list , mark_list)
    mark_list = j.main()
    subs = combine(mark_list , x)
    print(subs)

if __name__ == '__main__':
    a = time.time()
    x = "我是高锰酸根人们"
    main(x)
    b = time.time()
    print(b-a)
