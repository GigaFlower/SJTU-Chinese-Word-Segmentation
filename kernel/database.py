import os

PATH = os.path.split(os.path.realpath(__file__))[0]

class Data:
    def __init__(self):
        """
        There are three class properties.

        "file_word" represents the word lexicon file.
        "file_term" represents the term lexicon file.
        "file_character" represents the character lexicon file.
        """
        self.file_word = open(os.path.join(PATH, "wordlist_v2.txt"), "r", encoding="utf-16")
        self.file_term = open(os.path.join(PATH, "termlist.txt"), "r", encoding="utf-16")
        self.file_character = open(os.path.join(PATH, "characterlist.txt"), "r", encoding="utf-16")

    def split_into_list(self, file):
        """
        This function will split the lexicon into lots of lists.
        """
        string = file.read()
        list_split = string.split()
        return list_split

    def combine(self, list_split):
        """
        This function will combine the elements of the same word into a list in the
        form of name, probability and properties.
        """
        counter = -1
        word_list = []
        for element in list_split:
            if ord(element[0]) >= 128:
                # If a Chinese character is detected, it will be appended into a
                # new element, followed by its probability and properties.
                counter += 1
                word_list += [[]]
            word_list[counter].append(element)
        return word_list

    def relist(self, word_list):
        """
        This function will rearrange the words' name, probability and properties
        into three separate lists.
        """
        word = [element[0] for element in word_list]
        probability = [element[1] for element in word_list]
        properties = [element[2:] for element in word_list]
        return word, probability, properties

    def combine_cha(self, list_split):
        """
        This function will combine the elements of the same character into a list
        in the form of name and probability.
        """
        word = []
        probability = []
        for num in range(len(list_split)):
            if num % 2 == 0:
                word.append(list_split[num])
            else:
                probability.append(list_split[num])
        return word,probability

    def dictionary(self,list_a,list_b):
        """
        This function will make a dictionary for two lists.
        """
        dic=dict( zip(list_a, list_b) )
        return dic

    def solve_word(self):
        """
        This is the main structure of constructing the database of the words.

        Each word in the word file is made up of two characters.

        First, read the word file and split the content into lists.
        Then, combine the related lists of the same word into one list, and thus the
        whole list consists of many elements which represents a particular word.
        After that, rearrange the list so that three lists are created, including
        the word list, the probability list and the property list.
        Finally make the dictionary of the words and their probabilities.
        """
        list_spilt = self.split_into_list(self.file_word)
        word_list = self.combine(list_spilt)
        wd, pb, pro = self.relist(word_list)
        # "wd" means word, "pb" means probability, "pro" means property
        dic_pb = self.dictionary(wd,pb)
        self.file_word.close()
        return dic_pb

    def solve_term(self):
        """
        This is the main structure of constructing the database of the terms.

        "TERM" includes idioms, names of famous people and some fixed collocations.

        First, read the termword file and split the content into lists.
        Then, combine the related lists of the same word into one list, and thus the
        whole list consists of many elements which represents a particular word.
        After that, rearrange the list so that three lists are created, including
        the word list, the probability list and the property list.
        Finally make the dictionary of the words and their properties.
        """
        list_spilt = self.split_into_list(self.file_term)
        word_list = self.combine(list_spilt)
        wd, pb, pro = self.relist(word_list)
        # "wd" means word, "pb" means probability, "pro" means property
        length = len(pro)
        new_wd_list = []
        for num in range(length):
            new_wd_list.append( [wd[num] , pro[num]] )
        dic_term = dict(new_wd_list)
        self.file_term.close()
        return dic_term

    def solve_cha(self):
        """
        This is the main structure of constructing the database of the characters.

        First, read the character file and split the content into lists.
        Then, combine the related lists of the same character into one list, and
        thus the whole list consists of many elements which represents a particular
        character.
        After that, rearrange the list so that two lists are created, including
        the character list and the probability list.
        Finally make the dictionary of the charaters and their probabilities.
        """
        list_spilt = self.split_into_list(self.file_character)
        wd,prob = self.combine_cha(list_spilt)
        dic_cha = self.dictionary(wd, prob)
        self.file_character.close()
        return dic_cha

    def get_dictionary(self):
        dic_pb = self.solve_word()
        dic_term = self.solve_term()
        dic_cha = self.solve_cha()
        return dic_pb,dic_cha,dic_term

    if __name__ == '__main__':
        get_dictionary()
