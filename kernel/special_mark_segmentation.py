#_*_encoding:utf-8_*_
"""
Code responsible for service logic
"""

SEN_MARK = '，。？！……；'
# "Sentence mark"
# It is used in function "quot_string_set". If each is detected, it means the
# string between the quotation marks is regarded to be a sentence rather than
# a word.

class Special_mark_seg:
    """Special mark segmentation"""
    def __init__(self):
        """
        There are one class property.

        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        """
        self.mark_list = []

    def set_mark_list(self,counter,num):
        """
        This function will set the relationship between the characters in TERM
        as "bound".
        """
        for list_num in range(counter , counter + num):
            self.mark_list[list_num] = "bound"

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
            self.set_mark_list(counter, length + 1)
        else:
            pass

    def retrieve(self,string):
        """
        This function will retrieve the whole string from left to right to
        search whether the string contains the quotation marks and book marks,
         which will be handled by some further judgements.
        """
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
                            self.set_mark_list(num, search_num - num)
                        else:
                            pass
                except:
                    pass
            else:
                pass
        return self.mark_list
