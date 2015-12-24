
import math, os
from kernel import calculate

PATH = os.path.split(os.path.realpath(__file__))[0]


class Mi:
    """Mutual information of two Chinese character"""
    def __init__(self):
        """
        There are six class properties.

        "number_string" represents some special characters most of which has the
        meaning of numbers.
        "number_separate_string" represents some special characters, and when
        they follows the characters in "number_string", they tend to separate.
        "punctuation_string" represents some punctuations in the sentences which
        has the same usage of the separate mark.
        "dic_pb" is the dictionary with words and their probabilities.
        "dic_cha" is the dictionary with characters and their probabilities.
        "dic_term" is the dictionary with words marked with "TERM".
        """
        self.number_string = ""
        self.number_separate_string = ""
        self.punctuation_string = ""
        self.dic_pb = {}
        self.dic_cha = {}
        self.dic_term = {}

    def get_number_standard(self):
        file = open(os.path.join(PATH, "number_file.txt"), "r", encoding="utf-16")
        self.number_string = file.read()
        file.close()

    def get_number_separate(self):
        file = open(os.path.join(PATH, "number_separate_file.txt") , "r" , encoding = "utf-16")
        self.number_separate_string = file.read()

    def get_punc_standard(self):
        file = open(os.path.join(PATH, "punctuation_file_in_prob.txt"), "r", encoding="utf-16")
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

    def search_prob(self,certain_word):
        """
        This function will search for the probability of the certain word or
        character.
        """
        x = certain_word
        if len(x) == 1:
            try:
                if x in self.punctuation_string:
                    # if the character is a separation punctuation, then we
                    # should return a very big probability in order to make it
                    # separated.
                    return 9999999
                else:
                    p = self.dic_cha[x]
                    return int(p)
            except:
                # if the character is neither in the dictionary nor is a
                # separation punctuation, it will return 5 as the probability.
                return 5
        else:
            if x[0] in self.punctuation_string or x[1] in self.punctuation_string:
                    # if the word contains the separation punctuation, then we
                    # should return a very big probability in order to make it
                    # separated.
                    return 5
            elif x in self.dic_pb:
                p = int(self.dic_pb[x])
                if x[0] in self.number_string and x[1] in self.number_string:
                    # if the word's two characters are both number characters,
                    # they tend to be bound.
                    p = max( p + 3000000 , 2 * p )
                elif x[0] in self.number_string and x[1] not in self.number_separate_string:
                    # if the word's first character is number character, and the
                    # second character is not the one which tends to be
                    # separated when following the number character, it will
                    # return a big number which means they tend to be bound.
                    p = max( p + 300000 , 1.5 * p )
                else:
                    # if the word's first character is number character, but the
                    # second character is in the one which tends to be separated
                    # when following the number character, nothing will happen.
                    pass
            else:
                p = 5
                if x[0] in self.number_string and x[1] in self.number_string:
                    p = 3000000
                elif x[0] in self.number_string and x[1] not in self.number_separate_string:
                    p = 300000
                else:
                    pass
            return int(p)

    def calculate_mi(self,two_long_word):
        """
        This function will calculate the mi of the given two adjacent characters
        "xy".
        First, get x's, y's and xy's probabilities.
        Then calculate mi of "xy" by the formula:
            mi = "log2 ( p(xy) * 1000 / (p(x) * p(y)) )"
        """
        wd = two_long_word
        x = wd[0]
        y = wd[1]   # x means the first character, and y is the second character.
        prob_wd = self.search_prob(wd)
        prob_x = self.search_prob(x)
        prob_y = self.search_prob(y)
        mi = math.log(prob_wd * 1000 / (prob_x * prob_y), 2)
        return mi

    def get_mi(self, string_list):
        """
        This function will get the mi list.
        The result is a list including the 2-long word and its mi value.
        """
        string_with_mi_list = []
        for element in string_list:
            mi = self.calculate_mi(element)
            new_info_list = [element, mi]
            string_with_mi_list.append(new_info_list)
        return string_with_mi_list

    def get_mi_mean_and_derivation(self,string_with_mi_list):
        """
        This function is used to get the mis' mean and standard derivation for
        the judgement part.
        """
        mi_list = [x[1] for x in string_with_mi_list]
        mean = calculate.calculate_average(mi_list)
        standard_derivation = calculate.calculate_list_standard_derivation(mi_list)
        return mean, standard_derivation

    def mi_main(self,string):
        """
        This is the main structure of the mi calculation part.
        First get some special case data from some files.
        Then calculate the mi of all two-long words.
        And finally, calculate the mean and standard derivation of the whole mi
        list which will be used in the judgement part.
        """
        self.get_number_standard()
        self.get_number_separate()
        self.get_punc_standard()
        string_list = self.divide(string)
        string_with_mi_list = self.get_mi(string_list)
        mean, standard_derivation = self.get_mi_mean_and_derivation(string_with_mi_list)
        return mean, standard_derivation, string_with_mi_list
