
class TermSeg:
    """Term segmentation"""
    def __init__(self):
        """
        There are four class properties.

        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        "dic_pb" is the dictionary with words and their probabilities.
        "dic_cha" is the dictionary with characters and their probabilities.
        "dic_term" is the dictionary with words marked with "TERM".
        """
        self.mark_list = []
        self.dic_pb = {}
        self.dic_cha = {}
        self.dic_term = {}

    def set_mark_list(self,counter,num):
        """
        This function will set the relationship between the characters in TERM
        as "bound".
        """
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = "bound"

    def term_segmentation(self, counter, num, string):
        """
        This function will replace the term characters with the blanks in the
        same length in case that the term will interfere with the segmentation
        of other words.
        """
        if string[counter : counter + num] in self.dic_term:
            string = "".join([string[:counter]," " * num, string[counter + num:]])
            self.set_mark_list(counter,num)
        else:
            pass

    def retrieve(self,string):
        """
        This function will retrieve the whole string from 13 adjacent characters
        to 3, and judge whether the certain word is a TERM.
        """
        length = len(string)
        self.mark_list = [0] * (length - 1 )
        if length >= 13:
            for num in range(13,1,-1):
                for counter in range(0,length - num - 1):
                    self.term_segmentation(counter, num ,string)
        else:
            # If the length of the string is less than 13, retrieve from the
            # length number to 3.
            for num in range(length,1,-1):
                for counter in range(0,length - num + 1):
                    self.term_segmentation(counter, num ,string)
        return string, self.mark_list
