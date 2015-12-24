
class RuleSeg:
    """Rule of particular examples segmentation"""
    def __init__(self):
        """
        There are 2 class properties.

        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        "dic_rule" is the dictionary with the particular examples and their
        relationships.
        """
        self.mark_list = []
        self.dic_rule = {}

    def set_mark_list(self, counter, num, rule):
        """
        This function will set the relationship between the strings as the one
        in the rule dictionary.
        """
        for list_num in range(counter , counter + num - 1):
            self.mark_list[list_num] = rule[list_num - counter]

    def rule_segmentation(self, counter, num, string):
        """
        This function will judge whether there is a word in the rule dictionary.
        """
        particular_string = string[counter : counter + num]
        if particular_string in self.dic_rule:
            self.set_mark_list(counter, num, self.dic_rule[particular_string])
        else:
            pass

    def retrieve(self,string):
        """
        This function will retrieve the whole string from 6 adjacent characters
        to 2, and judge whether the certain word is in the rule dictionary.
        If it is in the rule dictionary, separate it according to the
        relationship given in the rule dictionary.
        """
        length = len(string)
        if length >= 6:
            for num in range(6,1,-1):
                for counter in range(0, length - num + 1):
                    self.rule_segmentation(counter, num ,string)
        else:
            # If the length of the string is less than 6, retrieve from the
            # length number to 2.
            for num in range(length,1,-1):
                for counter in range(0, length - num + 1):
                    self.rule_segmentation(counter, num ,string)
        return self.mark_list
