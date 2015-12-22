#_*_encoding:utf-8_*_
"""
Code responsible for service logic
"""

import time
import os
from kernel import database, dts_calculate, mi, judge, term_segmentation

SPLIT = '|'
PATH = os.path.split(os.path.realpath(__file__))[0]


class Segmentation:
    """This class handles all staff relating to segmentation"""
    def __init__(self):
        # Initialize lexicon
        self.lex = Lexicon()

        # Initialize rules
        self.rules = Rule()

        self.sen_punc_stan = open(os.path.join(PATH, "punctuation_standard_file.txt"), "r",
                             encoding="utf-16").read()
        # "sen_punc_stan" are sentence segment punctuations.
        self.d = database.Data()
        self.dic_pb, self.dic_cha, self.dic_term = self.d.get_dictionary()

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

        Example:
        >>> s = Segmentation()
        >>> s.sentence_segment("一，二三！四五，六七八。")
        ['一，', '二三！', '四五，', '六七八。']
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
        string_complete.append(substring)
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
        dts_mean, dts_standard_derivation, string_with_dtscore_list = self.dts.dts_calculate_main(string)

        self.set_class_property_dic(self.m)
        mi_mean, mi_standard_derivation, string_with_mi_list = self.m.mi_main(string)

        self.set_judge_property(dts_mean, dts_standard_derivation,
                                string_with_dtscore_list,
                                mi_mean, mi_standard_derivation,
                                string_with_mi_list, mark_list)
        mark_list = self.j.get_mark_list()

        subs = self.combine(mark_list, raw)
        return subs

    def combine(self, mark_list, string):
        """
        This function will combine the characters again according to the
        "mark_list". When it comes to "separated", the adjacent characters tend
        to separate and the separate mark will be added.
        In other cases, they tend to be bound.

        Example:
        >>> s = Segmentation()
        >>> s.combine(['separated','bound','separated','separated','bound'],'abcdef')
        'a|bc|d|ef'
        """
        length = len(string)
        subs = string[0]
        for num in range(length-1):
            if mark_list[num] == "separated":
                add = SPLIT + string[num + 1]
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

    def set_judge_property(self, dts_mean, dts_st_der, string_dts_list, mi_mean,
                            mi_st_der, string_mi_list, mark_list):
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
    def __init__(self):
        """
        Load a lexicon from a txt file.

        There are 7 class properties.

        "file_word" represents the original word lexicon file.
        "final_word_file" represents the final word lexicon file.
        "term_file" represents the final term lexicon file.
        "word_list" is the list with words and its probabilities.
        "term_list" is the list with terms and its properties.
        "sentence_list" is the list with strings.
        "dic_pb" is the dictionary, i.e., the word lexicon.
        """
        self.lex = []
        # src = open(filename, "r").read()
        # self.lex = src.split()

        self.file_word = open(os.path.join(PATH, "wordlist.txt"), "r", encoding="utf-16")
        self.final_word_file = open(os.path.join(PATH, "wordlist_v2.txt"), "r", encoding="utf-16")
        self.term_file = open(os.path.join(PATH, "termlist.txt"), "r", encoding="utf-16")
        self.word_list = []
        self.term_list = []
        self.sentence_list = []
        self.dic_pb = {}

    def split_into_list(self, string):
        """
        This function will split the lexicon into lots of lists.
        """
        list_split = string.split()
        return list_split

    def combine(self, list_split):
        """
        This function will combine the elements of the same word into a list in the
        form of name, probability and properties.
        """
        counter = -1
        for element in list_split:
            if ord(element[0]) >= 128:
                # If a Chinese character is detected, it will be appended into a
                # new element, followed by its probability and properties.
                counter += 1
                self.word_list += [[]]
            self.word_list[counter].append(element)

    def add_probability(self, problist):
        """
        This function will cut the words with more than 2 characters
        into several 2-long words.
        Then the word probability in the dictionary will be rewritten.
        """
        for element in problist:
            if len(element[0]) > 2:
                self.dic_pb.pop(element[0])
                # Remove the certain word with more than 2 characters from
                # the dictionary.
                for num in range(len(element[0]) - 1):
                    cut_element = element[0][num: num + 2]
                    if cut_element in self.dic_pb:
                        self.dic_pb[cut_element] += element[1]
                    else:
                        self.dic_pb[cut_element] = element[1]
                    # If the cut two adjacent characters are in the dictionary,
                    # then add the probability; otherwise, create the new word
                    # into the dictionary.

    def relist(self, word_list):
        """
        This function will relist the words' names and probabilities into two
        separate lists.
        """
        word = [element[0] for element in word_list]
        probability = [int(element[1]) for element in word_list]
        return word, probability

    def keep_term(self):
        """
        This function will keep the term lists which will be used to create the
        term lexicon.
        """
        for element in self.word_list:
            if element[2] == "TERM":
                sentence = " ".join(element)
                self.term_list.append(sentence)
            else:
                pass

    def rewrite_word_prob(self):
        """
        This function will rewrite the word probabilities.
        Those whose probabilities are between 3 to 7 will be rewritten.
        The formula is:
            new_prob = 100000 * (8 ** (7-n))
        """
        for element in self.word_list:
            if 3 <= int(element[1]) <= 7:
                n = int(element[1])
                element[1] = str(100000 * (8 ** (7 - n)))

    def sentence_join(self):
        """
        This function will join the sentences.
        """
        for element in self.word_list:
            element[1] = str(element[1])
            sentence = " ".join(element)
            self.sentence_list.append(sentence)

    def rewrite_lexicon(self):
        """
        This is the main structure of the lexicon rewrite part.

        First, read the original word lexicon and split the content into lists.
        Next, combine the related lists of the same word into one list, and thus
        the whole list consists of many elements which represents a particular word.
        Thirdly, keep the terms and write the term list into a file which is the
        term lexicon.
        Then, rearrange the list so that two lists are created, including the
        word list and the probability list.
        After that, cut the words with more than 2 characters into several
        2-long words, and change the probabilities of the words.
        Finally, combine the wordlist into a string and write into a file which
        is the word lexicon.
        """
        string = self.file_word.read()
        self.file_word.close()

        list_split = self.split_into_list(string)
        self.combine(list_split)

        self.keep_term()
        term_sentence = " ".join(self.term_list)
        self.term_file = open(os.path.join(PATH, "termlist.txt"), "w", encoding="utf-16")
        self.term_file.write(term_sentence)
        self.term_file.close()

        self.rewrite_word_prob()
        wd, pb = self.relist(self.word_list)
        word_with_pb_list = zip(wd, pb)
        self.dic_pb = dict(word_with_pb_list)
        self.word_list = [list(item) for item in self.dic_pb.items()]
        # This word_list is used as a comparing probability list, where words
        # with more than 2 characters are obtained.
        self.add_probability(self.word_list)
        self.word_list = [list(item) for item in self.dic_pb.items()]
        # This word_list is used as a lexicon list, which only has 2-long words.

        self.sentence_join()
        sentence = " ".join(self.sentence_list)

        self.final_word_file = open(os.path.join(PATH, "wordlist_v2.txt"), "w", encoding="utf-16")
        self.final_word_file.write(sentence)
        self.final_word_file.close()


class Rule:
    """This class represents a rule library"""
    pass

if __name__ == '__main__':
    l = Lexicon()
    l.rewrite_lexicon()

    a = time.time()
    s = Segmentation()
    print(s.word_segment("中华人民共和国斥资２．５亿打造航母。"))
    b = time.time()
    print("Time consumed: %.2fs" % (b-a))
