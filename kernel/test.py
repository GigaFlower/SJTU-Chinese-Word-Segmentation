"""
This file test the accuracy and efficiency of segmentation
Test corpus comes from ShanXi University
"""
import kernel
import re, time


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
    l = string.split(kernel.SPLIT)
    for i in l:
        end = start + len(i)
        ret.append((start, end))
        start = end
    return ret


def diff(ans: str, correct_ans: str) -> (int, int, int):
    """
    This function compare two segmentation result in detail
    It return three ints including:
    N : Total words in correct_ans
    c : how many words ans split out but not appear in correct_ans
    e : how many words ans split correctly
    """
    N = correct_ans.count(kernel.SPLIT) + 1
    e = 0
    c = 0

    l1 = convert_to_index_list(ans)
    l2 = convert_to_index_list(correct_ans)

    for wrd in l1:
        if wrd in l2:
            c += 1
        else:
            e += 1

    return N, c, e


def test(start=0, amount=20):
    """
    Do test according to test.txt and answer.txt
    :param amount:denote how many lines of tests you'd like to do,if -1,do every test.
    """
    t0 = time.time()

    seg = kernel.Segmentation()
    seg.set_rule_boolean([True, False, True])

    output = open("test_result600-1600.txt", 'w')
    src_file = open('test.txt', 'r', encoding='utf-16')
    ans_file = open('answer.txt', 'r', encoding='utf-16')

    test_cnt = 0
    N = 0  # Total words correct answer contains
    c = 0  # Words split correctly
    e = 0  # Words split wrong

    for i in range(start):
        src_file.readline()
        ans_file.readline()

    for line in src_file:
        test_cnt += 1
        if test_cnt > amount != -1:  # amount = -1 means do every test
            break
        ans = ans_file.readline().strip()
        ans = re.sub(r'\s+', kernel.SPLIT, ans)
        # Since answer.txt use double whitespace as split,first convert it to our split '|'
        ret = seg.word_segment(line.strip())
        dN, dc, de = diff(ret, ans)
        N += dN
        c += dc
        e += de
        if de == 0:
            tmp = '\nSentence #%d passed!\n' % (test_cnt+start)
            output.write(tmp)
            print(tmp)
        else:
            tmp = '\nSentence #%d failed!\n' % (test_cnt+start)
            tmp += 'Correct answer:\n'
            tmp += ans
            tmp += '\nYour answer:\n'
            tmp += ret
            tmp += '\n'
            output.write(tmp)
            print(tmp)

    t = time.time() - t0

    if amount == -1:
        amount = test_cnt - 1

    tmp = '\n\n'
    tmp += '=' * 40
    tmp += '\nAll %d tests done.\n' % amount
    tmp += 'Time consumed: %.3fs\n' % t
    tmp += 'In all %d words in correct answer\n' % N
    tmp += '%d words have been covered\n' % c
    tmp += 'While %d words in your result are split wrong\n' % e

    r = c / N
    p = c / (c + e)
    fm = 2 * p * r / (p + r)
    er = e / N

    tmp += '-' * 40
    tmp += '\nRecall:%.2f%%\n' % (r*100)
    tmp += 'Precision:%.2f%%\n' % (p*100)
    tmp += 'f-measure:%.2f%%\n' % (fm*100)
    tmp += 'Error Rate:%.2f%%\n' % (er*100)
    tmp += '=' * 20
    tmp += 'End'
    tmp += '=' * 20

    print(tmp)
    output.write(tmp)
    output.close()

if __name__ == '__main__':

    test(600, 1000)
