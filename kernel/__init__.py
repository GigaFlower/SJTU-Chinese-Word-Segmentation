#_*_encoding:utf-8_*_
"""
Code responsible for service logic
"""

import time
import os
from kernel import dts_calculate, mi, judge, segmentation_by_retrieve

SPLIT = '|'
PATH = os.path.split(os.path.realpath(__file__))[0]
# The path of this file regardless of operating system.


class Segmentation:
    """This class handles all staff relating to segmentation"""
    def __init__(self):
        # Initialize lexicon
        self.lexicon = Lexicon()
        self.lexicon.set_dictionary()

        # Initialize lexicon rewriting system.
        self.rewr_lexicon = Rewrite_Lexicon()
        self.rewr_lexicon.rewrite_lexicon()

        # Initialize particular situation rules
        self.parti_situ = Parti_situ()
        self.dic_situ = self.parti_situ.get_parti_situation()

        # Particular rule buttons
        self.rule_term = True  # Rule term segmentation
        self.rule_spec_mark = True  # Rule special mark segmentation
        self.rule_situation = True  # Rule particular situation

        self.sen_punc_stan = open(os.path.join(PATH, "punctuation_standard_file.txt"), "r",
                             encoding="utf-16")
        # "sen_punc_stan" contains sentence segment punctuations.

        self.r = segmentation_by_retrieve.Seg_By_Retrieve()
        self.dts = dts_calculate.Dts()
        self.m = mi.Mi()
        self.j = judge.Judge()

        self.term_VALVE = 7
        # Term segmentation VALVE: the terms whose probability level is less
        # than or equal to the VALVE will be recognized and separated.

    def sentence_segment(self, raw: str) -> list:
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
        punc_stan = open(os.path.join(PATH, "punctuation_standard_file.txt"), "r",
                             encoding="utf-16").read()
        for cha in raw:
            if cha == "\n":
                string_complete.append(substring)
                # The linebreak "\n" is not included.
                substring = ""
            else:
                substring += cha
                if cha in punc_stan:
                    string_complete.append(substring)
                    # If the sentence segment punctuations("\n" is excluded) are
                    # detected, the sentence should be cut here.
                    substring = ""
                else:
                    pass
        if substring != "":
            string_complete.append(substring)
            # If the string doesn't end up with the sentence segmentation
            # punctuation, append the last string.
        else:
            pass
        self.sen_punc_stan.close()
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
        mark_list = [0] * (len(raw) - 1)

        self.set_retrieve_class_property(mark_list)
        string_retrieve_seg, mark_list = self.r.retrieve(raw)

        string_aft_sep_punc, mark_list = self.separate_punc(string_retrieve_seg, mark_list)
        string = " " + string_aft_sep_punc + " "
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
        mark_list = self.rewrite_marklist(mark_list)

        subs = self.combine(mark_list, raw)
        return subs

    def set_retrieve_class_property(self, mark_list):
        """
        Set the properties of the class Seg_By_Retrieve in
        segmentation_by_retrieve.
        """
        self.r.mark_list = mark_list
        self.r.dic_term = self.lexicon.dic_term
        self.r.dic_situ = self.dic_situ
        self.r.term_VALVE = self.term_VALVE
        self.r.rule_term = self.rule_term
        self.r.rule_spec_mark = self.rule_spec_mark
        self.r.rule_situation = self.rule_situation

    def set_class_property_dic(self, instance):
        """
        "instance" is in the form of "self.xx"

        This function will set the dictionary properties of a particular
        instance.

        "dic_pb" is the dictionary with words and their probabilities.
        "dic_cha" is the dictionary with characters and their probabilities.
        "dic_term" is the dictionary with words marked with "TERM".
        """
        instance.dic_pb = self.lexicon.dic_pb
        instance.dic_cha = self.lexicon.dic_cha
        instance.dic_term = self.lexicon.dic_term

    def rewrite_marklist(self, mark_list):
        """
        This function will rewrite marklist.
        It will turn "left" into the mark of its left neighbor and "right" into
        the mark of its right neighbor.
        """
        length = len(mark_list)
        for num in range(length):
            if mark_list[num] == "left":
                mark_list[num] = mark_list[num - 1]
            elif mark_list[num] == "right":
                mark_list[num] = mark_list[num + 1]
            else:
                pass
        return mark_list

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
        for num in range(length - 1):
            if mark_list[num] in ["separated", "separated1", "separated2", "separated3"]:
                add = SPLIT + string[num + 1]
                subs += add
            else:
                subs += string[num + 1]
        return subs

    def separate_punc(self, string, mark_list):
        """
        This function recognizes the punctuations and separate them by setting
        their relationships with their neighbors in mark_list as "separated".
        Then they are replaced by blanks.
        """
        punc_file = open(os.path.join(PATH, "punctuation_file_in_prob.txt"), "r", encoding="utf-16")
        # "punc_file" contains punctuations.
        punc = punc_file.read()
        subs = ""
        length = len(string)
        for num in range(length):
            if string[num] not in punc:
                subs += string[num]
            else:
                subs += " "
                # If the relationship of the punctuations with their neighbors
                # are not set before, label their relationships with "separated".
                if num == 0 and mark_list[num] == 0:
                    # If it is the first character, only separate it with its
                    # right neighbor.
                    mark_list[num] = "separated"
                elif num == length - 1 and mark_list[num - 1] == 0:
                    # If it is the last character, only separate it with its
                    # left neighbor.
                    mark_list[num - 1] = "separated"
                elif 0 < num < length - 1:
                    # If it is the middle character, separate it with its both
                    # neighbors.
                    if mark_list[num - 1] == 0:
                        mark_list[num - 1] = "separated"
                    else:
                        pass
                    if mark_list[num] == 0:
                        mark_list[num] = "separated"
                    else:
                        pass
                else:
                    pass
        punc_file.close()
        return subs, mark_list

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

    def get_word_lexicon(self):
        """
        Only called by controller.
        This function will get the original wordlist.
        The wordlist is in the dictionary form.
        """
        dic_orgwd = self.rewr_lexicon.dic_contro_wd
        return dic_orgwd

    def get_term_lexicon(self):
        """
        Only called by controller.
        This function will get the term lexicon.
        The term lexicon is in the dictionary form.
        """
        dic_term = self.lexicon.dic_term
        return dic_term

    def get_situ(self):
        """
        Only called by controller.
        This function will get the particular situation lexicon.
        The particular situation lexicon is in the dictionary form.
        """
        dic_situ = self.dic_situ
        return dic_situ

    def get_rule_description(self):
        des = []
        des.append("Proper noun segmentation")
        des.append("Quotation intelligent identify")
        des.append("Particular situation segmentation")
        return des

    def set_rule_boolean(self, bools):
        """
        This function set whether rules are obeyed.
        length of bools is unchecked
        """
        self.rule_term = bools[0]  # Rule term segmentation
        self.rule_spec_mark = bools[1]  # Rule special mark segmentation
        self.rule_situation = bools[2]  # Rule particular situations

class Lexicon:
    def __init__(self):
        """
        There are 6 class properties.

        "file_word" represents the word lexicon file.
        "file_term" represents the term lexicon file.
        "file_character" represents the character lexicon file.
        "file_origin_word" represents the original complete word lexicon file.
        "dic_pb" is the dictionary with words and their probabilities.
        "dic_cha" is the dictionary with characters and their probabilities.
        "dic_term" is the dictionary with words marked with "TERM".
        """
        self.file_word = open(os.path.join(PATH, "wordlist_v2.txt"), "r", encoding="utf-16")
        self.file_term = open(os.path.join(PATH, "termlist.txt"), "r", encoding="utf-16")
        self.file_character = open(os.path.join(PATH, "characterlist.txt"), "r", encoding="utf-16")
        self.dic_pb = {}
        self.dic_cha = {}
        self.dic_term = {}

    def split_into_list(self, file):
        """
        This function will split the lexicon into lots of lists.
        """
        string = file.read()
        list_split = string.split()
        return list_split

    def combine(self, list_split):
        """
        This function will combine the elements of the same word into a list in the
        form of name, probability and properties.
        """
        counter = -1
        word_list = []
        for element in list_split:
            if ord(element[0]) >= 128:
                # If a Chinese character is detected, it will be appended into a
                # new element, followed by its probability and properties.
                counter += 1
                word_list += [[]]
            word_list[counter].append(element)
        return word_list

    def relist(self, word_list):
        """
        This function will rearrange the words' name, probability and properties
        into three separate lists.
        """
        word = [element[0] for element in word_list]
        probability = [element[1] for element in word_list]
        properties = [element[2:] for element in word_list]
        return word, probability, properties

    def combine_cha(self, list_split):
        """
        This function will combine the elements of the same character into a list
        in the form of name and probability.
        """
        word = []
        probability = []
        for num in range(len(list_split)):
            if num % 2 == 0:
                word.append(list_split[num])
            else:
                probability.append(list_split[num])
        return word,probability

    def dictionary(self,list_a,list_b):
        """
        This function will make a dictionary for two lists.
        """
        dic=dict( zip(list_a, list_b) )
        return dic

    def solve_word(self):
        """
        This is the main structure of constructing the database of the words.

        Each word in the word file is made up of two characters.

        First, read the word file and split the content into lists.
        Then, combine the related lists of the same word into one list, and thus the
        whole list consists of many elements which represents a particular word.
        After that, rearrange the list so that three lists are created, including
        the word list, the probability list and the property list.
        Finally make the dictionary of the words and their probabilities.
        """
        list_spilt = self.split_into_list(self.file_word)
        word_list = self.combine(list_spilt)
        wd, pb, pro = self.relist(word_list)
        # "wd" means word, "pb" means probability, "pro" means property
        dic_pb = self.dictionary(wd,pb)
        self.file_word.close()
        return dic_pb

    def solve_term(self):
        """
        This is the main structure of constructing the database of the terms.

        "TERM" includes idioms, names of famous people and some fixed collocations.

        First, read the termword file and split the content into lists.
        Then, combine the related lists of the same word into one list, and thus the
        whole list consists of many elements which represents a particular word.
        After that, rearrange the list so that three lists are created, including
        the word list, the probability list and the property list.
        Finally make the dictionary of the words and their probability levels.
        """
        list_spilt = self.split_into_list(self.file_term)
        word_list = self.combine(list_spilt)
        wd, pb, pro = self.relist(word_list)
        # "wd" means word, "pb" means probability, "pro" means property
        length = len(pro)
        new_wd_list = []
        for num in range(length):
            new_wd_list.append( [wd[num] , pb[num]] )
        dic_term = dict(new_wd_list)
        self.file_term.close()
        return dic_term

    def solve_cha(self):
        """
        This is the main structure of constructing the database of the characters.

        First, read the character file and split the content into lists.
        Then, combine the related lists of the same character into one list, and
        thus the whole list consists of many elements which represents a particular
        character.
        After that, rearrange the list so that two lists are created, including
        the character list and the probability list.
        Finally make the dictionary of the charaters and their probabilities.
        """
        list_spilt = self.split_into_list(self.file_character)
        wd,prob = self.combine_cha(list_spilt)
        dic_cha = self.dictionary(wd, prob)
        self.file_character.close()
        return dic_cha

    def set_dictionary(self):
        self.dic_pb = self.solve_word()
        self.dic_term = self.solve_term()
        self.dic_cha = self.solve_cha()


class Rewrite_Lexicon:
    """This class represents a lexicon library"""
    def __init__(self):
        """
        Load a lexicon from a txt file.

        There are 8 class properties.

        "file_word" represents the original word lexicon file.
        "final_word_file" represents the final word lexicon file.
        "term_file" represents the final term lexicon file.
        "word_list" is the list with words and its probabilities.
        "term_list" is the list with terms and its properties.
        "sentence_list" is the list with strings.
        "dic_pb" is the dictionary, i.e., the word lexicon.
        "dic_contro_wd" is the dictionary without terms and it will be given to
        controller.
        """
        self.file_word = open(os.path.join(PATH, "wordlist.txt"), "r", encoding="utf-16")
        self.final_word_file = open(os.path.join(PATH, "wordlist_v2.txt"), "r", encoding="utf-16")
        self.term_file = open(os.path.join(PATH, "termlist.txt"), "r", encoding="utf-16")
        self.word_list = []
        self.term_list = []
        self.sentence_list = []
        self.dic_pb = {}
        self.dic_contro_wd = {}

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

    def get_dic_contro_wd(self,dic):
        for item in dic:
            if 3 <= dic[item] <= 7:
                n = dic[item]
                self.dic_contro_wd[item] = 100000 * (8 ** (7 - n))
            else:
                self.dic_contro_wd[item] = dic[item]

    def relist(self, word_list):
        """
        This function will relist the words' names and probabilities into two
        separate lists.
        """
        new_list = []
        for element in word_list:
            if element[2] != "TERM":
                new_list.append([element[0] , int(element[1])])
            else:
                pass
        return new_list

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
        self.term_file = open(os.path.join(PATH, "termlist.txt"), "w+",
                                encoding="utf-16")
        self.term_file.write(term_sentence)
        self.term_file.close()

        self.rewrite_word_prob()
        word_with_pb_list = self.relist(self.word_list)
        self.dic_pb = dict(word_with_pb_list)

        self.get_dic_contro_wd(self.dic_pb)
        # To get the dictionary for controller.

        self.word_list = [list(item) for item in self.dic_pb.items()]
        # This word_list is used as a comparing probability list, where words
        # with more than 2 characters are obtained.
        self.add_probability(self.word_list)
        self.word_list = [list(item) for item in sorted(self.dic_pb.items())]
        # This word_list is used as a lexicon list, which only has 2-long words.

        self.sentence_join()
        sentence = " ".join(self.sentence_list)

        self.final_word_file = open(os.path.join(PATH, "wordlist_v2.txt"), "w+",
                                 encoding="utf-16")
        self.final_word_file.write(sentence)
        self.final_word_file.close()

    def add_word(self, list_of_word):
        """
        Only called by controller.

        This function will add a new word into wordlist through the program.

        The form of the parameter is [word name, probability level (range from 3
        to 7, 3 is the highest level), properties of the word (two or more
        properties are allowed)]:
            For example:
                list_of_word = ["我们", "3", "N"]
                or,
                list_of_word = ["因为", "3", "CONJ", "PREP"]
        """
        file_wordlist = open(os.path.join(PATH, "wordlist.txt"), "a",
                              encoding="utf-16")
        try:
            sentence = " ".join(list_of_word)
        except:
            sentence = ""
        sentence = " " + sentence
        file_wordlist.write(sentence)
        file_wordlist.close()

    def add_particular_situation(self, list_of_situation):
        """
        Only called by controller.

        This function will add a new particular situation into situation lexicon
        through the program.

        The form of the parameter is [string name, relationships (only contains
        "bound" and "separated" and they are separated by "," (this comma is in
        English form) )]:
            For example:
                list_of_situation = ["先后来到", "bound,separated,bound"]
        """
        file_situation = open(os.path.join(PATH, "particular_situation.txt"),
                                "a", encoding="utf-16")
        try:
            sentence = " ".join(list_of_situation)
        except:
            sentence = ""
        sentence = "\n" + sentence
        file_situation.write(sentence)
        file_situation.close()

class Parti_situ:
    """Particular situation"""
    def __init__(self):
        pass

    def combine_situ(self, list_split):
        """
        This function will combine the elements of the same word into a list
        in the form of items and relationship.
        """
        items = []
        relationship = []
        for num in range(len(list_split)):
            if num % 2 == 0:
                items.append(list_split[num])
            else:
                relationship.append(list_split[num])
        return items, relationship

    def rela_to_list(self, relationship):
        """
        This function will turn the relationships which are in the string form
        into lists.
        """
        new_list = []
        for element in relationship:
            element_aft_split = element.split(",")
            new_list.append(element_aft_split)
        return new_list

    def dictionary(self,list_a,list_b):
        """
        This function will make a dictionary for two lists.
        """
        dic=dict( zip(list_a, list_b) )
        return dic

    def get_parti_situation(self):
        """
        NOTE: The comma in the file "particular_situation.txt" MUST be in English form.

        This is the main structure of the particular situation getting procedure.

        The particular situation contains the correct segmentation of some
        particular examples, which can improve the precision of the whole
        segmentation to some extent.

        The situations are stored in the "particular_situation.txt". The system will first read it
        and split it into scores of lists. Then the list will be turned into a
        dictionary, which will be used in the segmentation part.
        """
        file_parti_situ = open(os.path.join(PATH, "particular_situation.txt"), "r", encoding="utf-16")
        situ_string = file_parti_situ.read()
        situ_list = situ_string.split()
        items, relationship = self.combine_situ(situ_list)
        relationship_in_list = self.rela_to_list(relationship)
        dic_situ = self.dictionary(items, relationship_in_list)
        return dic_situ

if __name__ == '__main__':

    a = time.time()
    s = Segmentation()
    print(s.word_segment("法国网球公开赛今天在巴黎西郊拉开战幕"))
    b = time.time()
    print("Time consumed: %.2fs" % (b-a))
