

def file_word():
    f = open("wordlist_v2.txt","r", encoding = "utf-16")
    return f

def file_termword():
    f = open("wordlist.txt","r", encoding = "utf-16")
    return f

def file_cha():
    f = open("characterlist.txt","r",encoding = "utf-16")
    return f

def split_into_list(f):
    """
    This function will split the lexicon into lots of lists.
    """
    s = f.read()
    l = s.split()
    return l

def combine(l):
    """
    This function will combine the elements of the same word into a list in the
    form of name, probability and properties.
    """
    c = -1
    wd_l = []
    for m in l:
        if ord(m[0]) >= 128:
            # If a Chinese character is detected, it will be appended into a
            # new element, followed by its probability and properties.
            c += 1
            wd_l += [[]]
        wd_l[c].append(m)
    return wd_l

def relist(l):
    """
    This function will rearrange the words' name, probability and properties
    into three separate lists.
    """
    wd = [x[0] for x in l]
    pb = [x[1] for x in l]
    pro = [x[2:] for x in l]
    return wd,pb,pro

def combine_cha(l):
    """
    This function will combine the elements of the same character into a list
    in the form of name and probability.
    """
    wd=[]
    prob=[]
    for i in range(len(l)):
        if i % 2 == 0:
            wd.append(l[i])
        else:
            prob.append(l[i])
    return wd,prob

def dictionary(a,b):
    """
    This function will make a dictionary for two lists.
    """
    dic=dict(zip(a,b))
    return dic

def solve_word():
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
    f_wd = file_word()
    l = split_into_list(f_wd)
    wd_l = combine(l)
    wd,pb,pro = relist(wd_l)
    dic_pb = dictionary(wd,pb)
    f_wd.close()
    return dic_pb

def solve_term():
    """
    This is the main structure of constructing the database of the terms.

    "TERM" includes idioms, names of famous people and some fixed collocations.

    First, read the termword file and split the content into lists.
    Then, combine the related lists of the same word into one list, and thus the
    whole list consists of many elements which represents a particular word.
    After that, rearrange the list so that three lists are created, including
    the word list, the probability list and the property list.
    Finally make the dictionary of the words and their probabilities.
    """
    f_wd = file_termword()
    l = split_into_list(f_wd)
    wd_l = combine(l)
    wd,pb,pro = relist(wd_l)
    length = len(pro)
    new_wd_list = []
    for num in range(length):
        if pro[num] == ["TERM"]:
            new_wd_list.append([wd[num],pro[num]])
    dic_term = dict(new_wd_list)
    return dic_term

def solve_cha():
    '''
    It's the process of creating a character dictionary.
    '''
    f_cha = file_cha()
    l = split_into_list(f_cha)
    wd,prob = combine_cha(l)
    dic_cha = dictionary(wd,prob)
    f_cha.close()
    return dic_cha

def database_main():
    dic_pb = solve_word()
    dic_term = solve_term()
    dic_cha = solve_cha()
    return dic_pb,dic_cha,dic_term

if __name__ == '__main__':
    database_main()
