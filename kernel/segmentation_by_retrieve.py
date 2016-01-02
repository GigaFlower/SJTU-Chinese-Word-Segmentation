#_*_encoding:utf-8_*_
"""
Code responsible for service logic
"""

SEN_MARK = '，。？！……；'
# "Sentence mark"
# It is used in function "Special_mark_seg.quot_string_set". If each is detected,
# it means the string between the quotation marks is regarded to be a sentence
# rather than a word.


class RetrieveSeg:
    """Segmentation by retrieve"""
    def __init__(self):
        """
        There are several class properties.

        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        "dic_term" is the dictionary with words marked with "TERM" and their
        probabilities.
        "dic_situ" is the dictionary with the particular examples and their
        relationships.
        "term_VALVE" is a VALVE that the terms whose probability level is less
        than or equal to it will be recognized and separated.
        """
        self.mark_list = []

        self.dic_term = {}
        self.dic_situ = {}

        self.term_VALVE = 7

        self.rule_term = True  # Rule term segmentation
        self.rule_spec_mark = True  # Rule special mark segmentation
        self.rule_situation = True  # Rule particular situation

    def get_wordlength(self):
        """
        This function will get all of the word length in the term dictionary and
        particular situations dictionary.
        """
        length_list = []
        for key in self.dic_term:
            word_length = len(key)
            if word_length not in length_list:
                length_list.append(word_length)
        for key in self.dic_situ:
            word_length = len(key)
            if word_length not in length_list:
                length_list.append(word_length)
        length_list.sort()
        length_list = length_list[::-1]
        # Reverse the order of the numbers in order to retrieve from long
        # strings to short ones.
        return length_list

    def set_bound_mark_list(self,counter,num):
        """
        This function will set the relationship between the characters in TERM
        or special punctuations as "bound".
        """
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = "bound"

    def term_segmentation(self, counter, num, string):
        """
        This function will replace the term characters whose probability level
        is less than or euqal to term_VALVE with the blanks in the same length
        in case that the term will interfere with the segmentation of other words.
        """
        part_string = string[counter : counter + num]
        if part_string in self.dic_term:
            if int(self.dic_term[part_string]) <= self.term_VALVE:
            # Judge whether the term's probability is lower than or equal to the
            # term VALVE.
                string = "".join([string[:counter]," " * num, string[counter + num:]])
                self.set_bound_mark_list(counter,num)
            else:
                pass
        else:
            pass

    def set_situ_mark_list(self, counter, num, situation):
        """
        This function will set the relationship between the strings as the one
        in the situation dictionary.
        """
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = situation[list_num - counter]

    def situation_segmentation(self, counter, num, string):
        """
        This function will judge whether there is a word in the situation
        dictionary.
        """
        particular_string = string[counter : counter + num]
        if particular_string in self.dic_situ:
            self.set_situ_mark_list(counter, num, self.dic_situ[particular_string])
        else:
            pass

    def quot_string_set(self, string, counter):
        """
        This function will judge whether the string between the quotation marks
        can be regarded as a word.
        If it is a word, three conditions should be met:
            1. The length of the word should be less than or equal to 6 characters.
            2. The string between the quotation marks shouldn't be empty.
            3. The string shouldn't contain the sentence separation marks.
        """
        mark = True
        # "mark" is used to show whether the string contains the sentence
        # separation marks.
        for character in string:
            if character in SEN_MARK:
                mark = False
            else:
                pass
        length = len(string)
        if 0 < length <= 6 and mark:
            self.set_bound_mark_list(counter, length + 2)
        else:
            pass

    def quot_retrieve(self, string):
        """
        This function will retrieve the whole string from left to right to
        search whether the string contains the quotation marks and book marks,
        which will be handled by some further judgments.
        """
        if self.rule_spec_mark:
            length = len(string)
            for num in range(length):
                if string[num] == '“':
                    # the quotation mark's part
                    try:
                        for search_num in range(num + 1, length):
                            if string[search_num] == '”':
                                self.quot_string_set(string[num + 1: search_num], num)
                            else:
                                pass
                    except:
                        pass
                elif string[num] == '《':
                    # the book mark's part
                    try:
                        for search_num in range(num + 1, length):
                            if string[search_num] == '》':
                                self.set_bound_mark_list(num, search_num - num + 1)
                            else:
                                pass
                    except:
                        pass
                else:
                    pass
        else:
            pass

    def term_and_situ_retrieve(self, string, length_list):
        """
        This function will retrieve the whole string for the certain numbers of
        characters, which is in length_list(it changes according to the termlist
        or situation list), and judge whether the certain word is a TERM or a
        particular situation.
        """
        length = len(string)
        if self.rule_situation and self.rule_term:
            for num in length_list:
                for counter in range(0, length - num + 1):
                    self.term_segmentation(counter, num, string)
                    self.situation_segmentation(counter, num, string)
        elif self.rule_situation and not self.rule_term:
            for num in length_list:
                for counter in range(0, length - num + 1):
                    self.situation_segmentation(counter, num, string)
        elif not self.rule_situation and self.rule_term:
            for num in length_list:
                for counter in range(0, length - num + 1):
                    self.term_segmentation(counter, num, string)
        else:
            pass
        return string, self.mark_list

    def retrieve(self, string):
        """
        The main structure of the retrieve process.

        This process contains term segmentation, particular situation
        segmentation and quotation segmentation.
        """
        length_list = self.get_wordlength()
        self.quot_retrieve(string)
        string, mark_list = self.term_and_situ_retrieve(string, length_list)
        return string, mark_list
