
import math
from hgs_part import database, calculate

dic_pb,dic_cha,dic_pro = database.database_main()


class mi:
    """Mutual information of two Chinese character"""
    def __init__(self):
        self.number_string = ""
        self.punctuation_string = ""

    def get_number_standard(self):
        file = open("number_file.txt", "r", encoding="utf-16")
        self.number_string = file.read()
        file.close()

    def get_punc_standard(self):
        file = open("punctuation_file_in_prob.txt", "r", encoding="utf-16")
        self.punctuation_string = file.read()
        file.close()

    def divide(self, string):
        """
        This function will divide the whole sentence into several lists,
        including the adjacent 2-word-long substring.
        """
        s = string
        subs = []
        for i in range(len(s) - 1):
            subs.append(s[i:i+2])
        return subs

    def search_prob(self, certain_word):
        """
        This function will search for the probability of the certain word or character.
        """
        global dic_pb,dic_cha
        x = certain_word
        if len(x) == 1:
            try:
                if x in self.punctuation_string:
                    return 9999999
                else:
                    p=dic_cha[x]
                    return int(p)
            except:
                return 5
        else:
            if x in dic_pb:
                p = int(dic_pb[x])
                if x[0] in self.number_string and x[1] in self.number_string:
                    p = max(p + 30000000, 2 * p)
                elif x[0] in self.number_string:
                    p = max(p + 3000000, 1.5 * p)
                else:
                    pass
            else:
                p = 5
                if x[0] in self.number_string and x[1] in self.number_string:
                    p = 30000000
                elif x[0] in self.number_string:
                    p = 3000000
                else:
                    pass
            return int(p)

    def calculate_mi(self,two_long_word):
        wd = two_long_word
        x = wd[0]
        y = wd[1]   # x means the first character, and y is the second character.
        prob_wd = self.search_prob(wd)
        prob_x = self.search_prob(x)
        prob_y = self.search_prob(y)
        mi = math.log2(prob_wd * 1000 / ( prob_x * prob_y )
        return mi

    def get_mi(self, string_list):
        string_with_mi_list = []
        for element in string_list:
            mi = self.calculate_mi(element)
            new_info_list = [element,mi]
            string_with_mi_list.append(new_info_list)
        return string_with_mi_list

    def get_mi_mean_and_derivation(self,string_with_mi_list):
        mi_list = [x[1] for x in string_with_mi_list]
        mean = calculate.calculate_average(mi_list)
        standard_derivation = calculate.calculate_list_standard_derivation(mi_list)
        return mean,standard_derivation

    def mi_main(self,string):
        self.get_number_standard()
        self.get_punc_standard()
        string_list = self.divide(string)
        string_with_mi_list = self.get_mi(string_list)
        mean,standard_derivation = self.get_mi_mean_and_derivation(string_with_mi_list)
        return mean,standard_derivation,string_with_mi_list
