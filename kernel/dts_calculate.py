

import calculate
import math


class Dts:
    """Delta t-score of two Chinese character"""
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
        file = open("number_file.txt" , "r" , encoding = "utf-16")
        self.number_string = file.read()

    def get_number_separate(self):
        file = open("number_separate_file.txt" , "r" , encoding = "utf-16")
        self.number_separate_string = file.read()

    def get_punc_standard(self):
        file = open("punctuation_file_in_prob.txt","r", encoding = "utf-16")
        self.punctuation_string = file.read()

    def divide(self,string,wd_width):
        """
        This function will divide the whole sentence into several lists,
        including the adjacent n-word-long substring.
        """
        s = string
        n = wd_width
        subs = []
        length = len(s)
        for i in range(length - n + 1):
            subs.append(s[i:i + n])
        return subs

    def search_prob(self,certain_word):
        """
        This function will search for the probability of the certain word
        or character.
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

    def get_two_long_wd_prob(self,string):
        """
        This function is used to get all the two adjacent characters'
        probabilities in the given string from the dictionary.
        The result is in the list form.
        """
        two_long_word_list = self.divide(string,2)
        prob_list = []
        for element in two_long_word_list:
            prob = self.search_prob(element)
            prob_list.append(prob)
        return prob_list

    def get_var(self,xy,prob_xy):
        """
        This function is used to get the variance of a particular word in the
        dictionary.
        The variance is calculated in the way following.
        First search for the word in the dictionary including either of the two
         characters in the given word "xy", and sum their probabilities up.
        Then calculate the average.
        Finally, calculate the variance of xy.
        """
        sum = 0
        c = 0
        try:
            for word in self.dic_pb:
                if xy[0] in word or xy[1] in word:
                    k = self.dic_pb[word]
                    sum += int(self.dic_pb[word])
                    c += 1
                else:
                    pass
            average = sum / c
            var = (prob_xy - average) ** 2 / c
        except:
            var = 1000000000000
            # If no words include either of the character in "xy", then a number
            # will be returned.
        return var

    def get_tscore(self,string,prob_list):
        """
        This function will calculate the tscore of the given three adjacent
        characters "xyz".
        First, get xy's and yz's probabilities.
        Then calculate xy's and yz's variances.
        Finally, get the tscore of "xyz" by the formula:
            tscore = "( p(yz) - p(xy) ) / sqrt( var(xy) + var(yz) )"
        The result is a list with the string "xyz" and its tscore.
        """
        three_long_word_list = self.divide(string,3)
        length = len(three_long_word_list)
        string_with_tscore_list = []
        for num in range(length):
            wd = three_long_word_list[num]
            xy = wd[0:2]  # xy means the first two characters.
            yz = wd[1:3]  # yz means the last two characters.
            prob_xy = prob_list[num]
            prob_yz = prob_list[num + 1]
            var_xy = self.get_var(xy, prob_xy)
            var_yz = self.get_var(yz, prob_yz)
            tscore = (prob_yz - prob_xy) / math.sqrt( var_xy + var_yz )
            new_info_list = [wd,tscore]
            string_with_tscore_list.append(new_info_list)
        return string_with_tscore_list

    def get_dtscore(self,string,string_with_tscore_list):
        """
        This function will calculate the tscore of the given four adjacent
        characters "vxyz".
        First, get vxy's and xyz's tscores.
        Then calculate dtscore by the formula:
            tscore = "tscore(vxy) - tscore(xyz)".\
        The result is a list with the string "vxyz" and its dtscore.
        """
        four_long_word_list = self.divide(string,4)
        length = len(four_long_word_list)
        string_with_dtscore_list = []
        for num in range(length):
            wd = four_long_word_list[num]
            dtscore = string_with_tscore_list[num][1] - string_with_tscore_list[num + 1][1]
            # dtscore(x: y) = tscore(x) - tscore(y)
            new_info_list = [wd,dtscore]
            string_with_dtscore_list.append(new_info_list)
        return string_with_dtscore_list

    def delete_including_punc_part_in_dtslist(self,string_with_dtscore_list):
        """
        This function is used to delete the words including the separation
        punctuations, and otherwise these words will interfere the mean and
        standard derivation and further interfere the judgement.
        """
        new_list = []
        for element in string_with_dtscore_list:
            if element[0][0] in self.punctuation_string and element[0][1] not in self.punctuation_string:
                new_list.append(element[1])
            else:
                pass
        return new_list

    def get_dtscore_mean_and_derivation(self,string_with_dtscore_list):
        """
        This function is used to get the dtscores' mean and standard derivation
        for the judgement part.
        """
        dtscore_list = self.delete_including_punc_part_in_dtslist(string_with_dtscore_list)
        mean = calculate.calculate_average(dtscore_list)
        standard_derivation = calculate.calculate_list_standard_derivation(dtscore_list)
        return mean,standard_derivation

    def dts_calculate_main(self,string):
        """
        This is the main structure of the dtscore calculation part.
        First get some special case data from some files.
        Then get the probabilities of each two-long word.
        After that, calculate the tscores and dtscores.
        And finally, calculate the mean and standard derivation of the whole
        dtscores list which will be used in the judgement part.
        """
        self.get_number_standard()
        self.get_number_separate()
        self.get_punc_standard()
        prob_list = self.get_two_long_wd_prob(string)
        string_with_tscore_list = self.get_tscore(string,prob_list)
        string_with_dtscore_list = self.get_dtscore(string,string_with_tscore_list)
        mean,standard_derivation = self.get_dtscore_mean_and_derivation(string_with_dtscore_list)
        return mean,standard_derivation,string_with_dtscore_list
