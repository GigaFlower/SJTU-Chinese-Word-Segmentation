

from . import database

dic_pb,dic_cha,dic_term = database.database_main()
"""
"dic_pb" is the dictionary with words and their probabilities.
"dic_cha" is the dictionary with characters and their probabilities.
"dic_term" is the dictionary with words marked with "TERM".
"""


class term_seg:
    def __init__(self):
        self.mark_list = []

    def set_mark_list(self,counter,num):
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = "bound"

    def term_segmentation(self,string):
        length = len(string)
        self.mark_list = [0] * length
        if length >= 13:
            for num in range(13,2,-1):
                for counter in range(0,length - num - 1):
                    if string[counter : counter + num] in dic_term:
                        string = "".join([string[:counter]," " * num, string[counter + num:]])
                        self.set_mark_list(counter,num)
                    else:
                        pass
        else:
            for num in range(length,2,-1):
                for counter in range(0,length - num + 1):
                    if string[counter : counter + num] in dic_term:
                        string = "".join([string[:counter]," " * num, string[counter + num:]])
                        self.set_mark_list(counter,num)
                    else:
                        pass
        return string, self.mark_list