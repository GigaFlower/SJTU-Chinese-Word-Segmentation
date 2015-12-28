
class PartSituSeg:
    """Rule of particular situations segmentation"""
    def __init__(self):
        """
        There are 2 class properties.

        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        "dic_situ" is the dictionary with the particular examples and their
        relationships.
        """
        self.mark_list = []
        self.dic_situ = {}

    def set_mark_list(self, counter, num, situation):
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
            self.set_mark_list(counter, num, self.dic_situ[particular_string])
        else:
            pass

    def retrieve(self,string):
        """
        This function will retrieve the whole string from 6 adjacent characters
        to 2, and judge whether the certain word is in the situation dictionary.
        If it is in the situation dictionary, separate it according to the
        relationship given in the situation dictionary.
        """
        length = len(string)
        if length >= 6:
            for num in range(6,1,-1):
                for counter in range(0, length - num + 1):
                    self.situation_segmentation(counter, num ,string)
        else:
            # If the length of the string is less than 6, retrieve from the
            # length number to 2.
            for num in range(length,1,-1):
                for counter in range(0, length - num + 1):
                    self.situation_segmentation(counter, num ,string)
        return self.mark_list
