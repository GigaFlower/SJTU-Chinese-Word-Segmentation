

import database,math,calculate

dic_pb,dic_cha,dic_pro = database.database_main()

def divide(string,wd_width):
    '''
    This function will divide the whole sentence into several lists, including the adjacent n-word-long substring.
    '''
    s = string
    n = wd_width
    subs = []
    length = len(s)
    for i in range(length - n + 1):
        subs.append(s[i:i + n])
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

def get_two_long_wd_prob(string):
    two_long_word_list = divide(string,2)
    prob_list = []
    for element in two_long_word_list:
        prob = search_prob(element)
        prob_list.append(prob)
    return prob_list

def get_prob_average(prob_list):
    prob_average = calculate.calculate_average(prob_list)
    return prob_average

def get_tscore(string,prob_list,prob_average):
    three_long_word_list = divide(string,3)
    length = len(three_long_word_list)
    string_with_tscore_list = []
    for num in range(length):
        wd = three_long_word_list[num]
        xy = wd[0:2]  # xy means the first two characters.
        yz = wd[1:3]  # yz means the last two characters.
        prob_xy = prob_list[num]
        prob_yz = prob_list[num + 1]
        var_xy = (prob_xy - prob_average) ** 2  / (length + 1)  # len(prob_list) = the number of two-long words = len(three_long_word_list) + 1
        var_yz = (prob_yz - prob_average) ** 2  / (length + 1)
        tscore = (prob_yz - prob_xy) / math.sqrt( var_xy + var_yz)
        new_info_list = [wd,tscore]
        string_with_tscore_list.append(new_info_list)
    return string_with_tscore_list

def get_dtscore(string,string_with_tscore_list):
    four_long_word_list = divide(string,4)
    length = len(four_long_word_list)
    string_with_dtscore_list = []
    for num in range(length):
        wd = four_long_word_list[num]
        dtscore = string_with_tscore_list[num][1] - string_with_tscore_list[num + 1][1]   # dtscore(x: y) = tscore(x) - tscore(y)
        new_info_list = [wd,dtscore]
        string_with_dtscore_list.append(new_info_list)
    return string_with_dtscore_list

def get_dtscore_mean_and_derivation(string_with_dtscore_list):
    dtscore_list = [x[1] for x in string_with_dtscore_list]
    mean = calculate.calculate_mean(dtscore_list)
    standard_derivation = calculate.calculate_list_standard_derivation(dtscore_list)
    return mean,standard_derivation

def dts_calculate_main(string):
    prob_list = get_two_long_wd_prob(string)
    prob_average = get_prob_average(prob_list)   # Get the probability average value as it will be used in calculating tscore.
    string_with_tscore_list = get_tscore(string,prob_list,prob_average)
    string_with_dtscore_list = get_dtscore(string,string_with_tscore_list)
    mean,standard_derivation = get_dtscore_mean_and_derivation(string_with_dtscore_list)
    return mean,standard_derivation,string_with_dtscore_list

if __name__ == '__main__':
    dts_calculate_main(string)