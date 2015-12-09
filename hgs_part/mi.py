

import database,math,calculate

dic_pb,dic_cha,dic_pro = database.database_main()

def divide(string):
    '''
    This function will divide the whole sentence into several lists, including the adjacent 2-word-long substring.
    '''
    s = string
    subs = []
    length = len(s)
    for i in range(len(s) - 1):
        subs.append(s[i:i+2])
    return subs

def search_prob(certain_word):
    '''
    This function will search for the probability of the certain word or character.
    '''
    global dic_pb,dic_cha
    x = certain_word
    if len(x) == 1:
        try:
            p=dic_cha[x]
            return int(p)
        except:
            return 5
    else:
        try:
            p=dic_pb[x]
            return int(p)
        except:
            return 5

def calculate_mi(two_long_word):
    wd = two_long_word
    x = wd[0]
    y = wd[1]   # x means the first character, and y is the second character.
    prob_wd = search_prob(wd)
    prob_x = search_prob(x)
    prob_y = search_prob(y)
    mi = math.log2( prob_wd * 1000 / ( prob_x * prob_y ))
    return mi

def get_mi(string_list):
    string_with_mi_list = []
    for element in string_list:
        mi = calculate_mi(element)
        new_info_list = [element,mi]
        string_with_mi_list.append(new_info_list)
    return string_with_mi_list

def get_mi_mean_and_derivation(string_with_mi_list):
    mi_list = [x[1] for x in string_with_mi_list]
    mean = calculate.calculate_mean(mi_list)
    standard_derivation = calculate.calculate_list_standard_derivation(mi_list)
    return mean,standard_derivation

def mi_main(string):
    string_list = divide(string)
    string_with_mi_list = get_mi(string_list)
    mean,standard_derivation = get_mi_mean_and_derivation(string_with_mi_list)
    return mean,standard_derivation,string_with_mi_list

if __name__ == '__main__':
    mi_main(string)
