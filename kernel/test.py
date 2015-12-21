"""
This file test the accuracy and efficiency of segmentation
Test corpus comes from ShanXi University
"""
import kernel
import re, time

SPLIT = '|'


def record_time(method):
    """This function extend function with the ability of recording the time consumed"""
    def new_method(*args):
        t0 = time.time()
        method(*args)
        print("Time consumed:%.3fs" % (time.time()-t0))
    return new_method


@record_time
def test(amount=20):
    """
    Do test according to test.txt and answer.txt
    :param amount:denote how many lines of tests you'd like to do,if -1,do every test.
    """
    seg = kernel.Segmentation()

    src_file = open('test.txt', 'r', encoding='utf-16')
    ans_file = open('answer.txt', 'r', encoding='utf-16')

    test_cnt = 0
    N = 0  # Total words correct answer contains
    c = 0  # Words split correctly
    e = 0  # Words split wrong

    for line in src_file:
        test_cnt += 1
        if test_cnt > amount != -1:  # amount = -1 means do every test
            break

        ans = ans_file.readline()
        ans = re.sub(r'\s+', SPLIT, ans)
        # Since answer.txt use double whitespace as split,first convert it to our split '|'

        ret = seg.word_segment(line)

        dN, dc, de = diff(ret, ans)
        N += dN
        c += dc
        e += de
        if de == 0:
            print('Sentence #%d passed!' % test_cnt)
        else:
            print('Sentence #%d failed!' % test_cnt)
            print('Correct answer:')
            print(ans)
            print('Your answer:')
            print(ret)

    if amount == -1:
        amount = test_cnt - 1
    print('All %d tests done.' % amount)
    print('In all %d words in correct answer' % N)
    print('%d words have been covered' % c)
    print('While %d words are split wrong' % e)

    r = c / N
    p = c / (c + e)
    fm = 2 * p * r / (p + r)
    er = e / N

    print('Recall:%.2f%%' % r*100)
    print('Precision:%.2f%%' % p*100)
    print('f-measure:%.2f' % fm)
    print('Error Rate:%.2f%%' % er)


# def convert_to_mark_list(string: str) -> list:
#     """
#     This function convert a segmentation result back to a list of
#     'b' stands for 'bounded' and 's' for 'separated'
#     for every position between two character.
#     Used to compare two segmentation result in detail in func diff()
#
#     Examples:
#     if SPLIT == '|'
#     >>> convert_to_mark_list("ab|cd|e|f|g")
#     ['b','s','b','s','s','s']
#     """
#     ret = []
#     ind = 0
#     while ind < len(string)-1:
#         if string[ind+1] != SPLIT:
#             ret.append('b')
#         else:
#             ret.append('s')
#             ind += 1
#         ind += 1
#     return ret


def convert_to_index_list(string: str) -> list:
    """
    This function convert a segmentation result to a list of start and end index of every word
    Used to compare two segmentation result in detail in func diff()

    Examples:
    if SPLIT == '|'
    >>> convert_to_index_list("ab|cd|e|fgh")
    [(0,2),(2,4),(4,5),(5,8)]
    """
    ret = []
    start = 0
    l = string.split(SPLIT)
    for i in l:
        end = start + len(i)
        ret.append((start, end))
        start = end
    return ret


# def diff(ans: str, correct_ans: str) -> (int, int):
#     """
#     This function compare two segmentation result in detail
#     It return how many mistakes 'ans' has made,including
#     a.The split that correct_ans has but ans doesn't i.e. missing splits
#     b.The split that correct_ans doesn't but ans has i.e. Unnecessary splits
#     """
#     l1 = convert_to_mark_list(ans)
#     l2 = convert_to_mark_list(correct_ans)
#
#     assert(len(l1) == len(l2))
#
#     mis = 0  # Missing splits
#     uny = 0  # Unnecessary splits
#     for i in range(len(l1)):
#         if l2[i] == 's' and l1[i] == 'b':
#             mis += 1
#         elif l2[i] == 'b' and l1[i] == 's':
#             uny += 1
#
#     return mis, uny
#

def diff(ans: str, correct_ans: str) -> (int, int, int):
    N = correct_ans.count(SPLIT) + 1   # how many words correct_ans contains
    e = 0  # how many words ans split wrong
    c = 0  # how many words ans split correctly

    l1 = convert_to_index_list(ans)
    l2 = convert_to_index_list(correct_ans)

    for wrd in l1:
        if wrd in l2:
            c += 1
        else:
            e += 1

    return N, c, e

if __name__ == '__main__':
    test()