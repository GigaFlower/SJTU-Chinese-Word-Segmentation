#_*_encoding:utf-8_*_
"""
Code responsible for service logic
"""

import time
import database, dts_calculate, mi, judge, term_segmentation


class Segmentation:
    """This class handles all staff relating to segmentation"""
    def __init__(self):
        # Initialize lexicon
        self.lex = Lexicon("lexicon.txt")

        # Initialize rules
        self.rules = Rule()

        self.sen_punc_stan = open("punctuation_standard_file.txt", "r",
                             encoding="utf-16").read()
        # "sen_punc_stan" are sentence segment punctuations.
        self.dic_pb, self.dic_cha, self.dic_term = database.get_dictionary()

        self.t = term_segmentation.Term_seg()
        self.dts = dts_calculate.Dts()
        self.m = mi.Mi()
        self.j = judge.Judge()

    def sentence_segment(self, raw: str) -> str:
        """
        This function will cut the whole string into several sentences according
        to the sentence segment punctuations.
        The punctuations are reserved, but there exists a special case that "\n"
        should be deleted.
        The completed sentences will be put in the list "s_complete".
        """
        substring = ""
        string_complete = []
        for cha in raw:
            if cha == "\n":
                string_complete.append(substring)
                # The linebreak "\n" is not included.
                substring = ""
            else:
                substring += cha
                if cha in self.sen_punc_stan:
                    string_complete.append(substring)
                    # If the sentence segment punctuations("\n" is excluded) are
                    # detected, the sentence should be cut here.
                    substring = ""
                else:
                    pass
        return string_complete

    def word_segment(self, raw: str) -> str:

        """
        This is the main structure of the word segmentation part.

        First, calculate the mi and the dt-score of each word.
        Then, then all the information will be sent to judge.py and in the file
        judge.py, there are three rounds judging whether the two adjacent
        characters should be bound or separated.
        Finally, the relationships between each two adjacent characters will be
        sent back, and through the "combine" function, the separate characters
        will be combined again with the separate mark "|".
        """


        self.set_class_property_dic(self.t)
        string_aft_termseg, mark_list = self.t.retrieve(raw)

        string = " " + string_aft_termseg + " "
        # Add " " in front of  the first character and behind the last character,
        # which will be used as an auxiliary in the calculation of mi and dtscore.

        self.set_class_property_dic(self.dts)
        dts_mean , dts_standard_derivation , string_with_dtscore_list = self.dts.dts_calculate_main(string)

        self.set_class_property_dic(self.m)
        mi_mean , mi_standard_derivation , string_with_mi_list = self.m.mi_main(string)

        self.set_judge_property(dts_mean,dts_standard_derivation,
                                string_with_dtscore_list ,
                                mi_mean,mi_standard_derivation ,
                                string_with_mi_list , mark_list)
        mark_list = self.j.get_mark_list()

        subs = self.combine(mark_list , raw)
        return subs

    def combine(self,mark_list,string):

        """
        This function will combine the characters again according to the
        "mark_list". When it comes to "separated", the adjacent characters tend
        to separate and the separate mark will be added.
        In other cases, they tend to be bound.
        """

        length = len(string)
        subs = string[0]
        for num in range(length-1):
            if mark_list[num] == "separated":
                add = "|" + string[num + 1]
                subs += add
            else:
                subs += string[num + 1]
        return subs

    def set_class_property_dic(self, instance):
        """
        "instance" is in the form of "self.xx"

        This function will set the dictionary properties of a particular
        instance.

        "dic_pb" is the dictionary with words and their probabilities.
        "dic_cha" is the dictionary with characters and their probabilities.
        "dic_term" is the dictionary with words marked with "TERM".
        """
        instance.dic_pb = self.dic_pb
        instance.dic_cha = self.dic_cha
        instance.dic_term = self.dic_term

    def set_judge_property(self,dts_mean,dts_st_der,string_dts_list,mi_mean,
                            mi_st_der,string_mi_list,mark_list):

        """
        This function will be used to set the properties of the class "judge" in
        judge.py.
        """

        self.j.dts_mean = dts_mean
        self.j.dts_standard_derivation = dts_st_der
        self.j.dts_list = [x[1] for x in string_dts_list]
        # Only sending the dts_list with only numbers to judge.py

        self.j.mi_mean = mi_mean
        self.j.mi_standard_derivation = mi_st_der
        mi_list = [x[1] for x in string_mi_list]
        # Only sending the mi_list with only numbers to judge.py
        self.j.mi_list = mi_list[1:-1]
        # The first and the last element in mi_list contains the blank,
        # so it is of no use and should be abandoned.

        self.j.mark_list = mark_list

class Lexicon:
    """This class represents a lexicon library"""
    def __init__(self, filename):
        """Load a lexicon from a txt file"""
        self.lex = []
        #src = open(filename, "r").read()
        #self.lex = src.split()


class Rule:
    """This class represents a rule library"""
    pass

a=time.time()
s=Segmentation()
print(s.word_segment("李克强与习近平会晤，共同磋商奔向太阳大计"))
b=time.time()
print(b-a)