

class Term_seg:
    def __init__(self):
        self.mark_list = []
        self.dic_pb = {}
        self.dic_cha = {}
        self.dic_term = {}

    def set_mark_list(self,counter,num):
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = "bound"

    def term_segmentation(self, counter, num, string):
        if string[counter : counter + num] in self.dic_term:
            string = "".join([string[:counter]," " * num, string[counter + num:]])
            self.set_mark_list(counter,num)
        else:
            pass

    def retrieve(self,string):
        length = len(string)
        self.mark_list = [0] * length
        if length >= 13:
            for num in range(13,2,-1):
                for counter in range(0,length - num - 1):
                    self.term_segmentation(counter, num ,string)
        else:
            for num in range(length,2,-1):
                for counter in range(0,length - num + 1):
                    self.term_segmentation(counter, num ,string)
        return string, self.mark_list
