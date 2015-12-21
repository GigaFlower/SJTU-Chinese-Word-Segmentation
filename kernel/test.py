"""
This file test the accuracy and efficiency of segmentation
Test corpus comes from ShanXi University
"""
import kernel
import re, time

SPLIT = '|'


def record_time(method):
    def new_method(*args):
        t0 = time.time()
        method(*args)
        print("Time consumed:%.3fs" % (time.time()-t0))
    return new_method


@record_time
def test(amount=20):
    seg = kernel.Segmentation()

    src_file = open('test.txt', 'r', encoding='utf-16')
    ans_file = open('answer.txt', 'r', encoding='utf-16')

    test_cnt = 0
    mis_cnt = 0  # Missing splits
    uny_cnt = 0  # Unnecessary splits
    total_cnt = 0

    for line in src_file:
        test_cnt += 1
        if test_cnt > amount:
            break

        ans = ans_file.readline()
        ans = re.sub(r'\s+', SPLIT, ans)

        ret = seg.word_segment(line)

        total_cnt += ans.count(SPLIT)
        mistakes = diff(ret, ans)
        mis_cnt += mistakes[0]
        uny_cnt += mistakes[1]
        if sum(mistakes) == 0:
            print('Sentence #%d passed!' % test_cnt)
        else:
            print('Sentence #%d failed!' % test_cnt)
            print('Correct answer:')
            print(ans)
            print('Your answer:')
            print(ret)

    print('All %d tests done.' % amount)
    print('In all %d splits' % total_cnt)
    print('%d splits are missed and' % mis_cnt)
    print('%d unnecessary splits are made' % uny_cnt)

    precision = 1-(mis_cnt+uny_cnt)/total_cnt
    precision *= 100
    print('Precision:%.2f%%' % precision)


def convert_to_mark_list(string: str) -> list:
    """
    This function convert a segmentation result back to a list of
    'b' stands for 'bounded' and 's' for 'separated'
    for every position between two character.
    Used to compare two segmentation result in detail in func diff()

    Examples:
    if SPLIT == '|'
    >>> convert_to_mark_list("ab|cd|e|f|g")
    ['b','s','b','s','s','s']
    """
    ret = []
    ind = 0
    while ind < len(string)-1:
        if string[ind+1] != SPLIT:
            ret.append('b')
        else:
            ret.append('s')
            ind += 1
        ind += 1
    return ret


def diff(ans: str, correct_ans: str) -> (int, int):
    """
    This function compare two segmentation result in detail
    It return how many mistakes 'ans' has made,including
    a.The split that correct_ans has but ans doesn't i.e. missing splits
    b.The split that correct_ans doesn't but ans has i.e. Unnecessary splits
    """
    l1 = convert_to_mark_list(ans)
    l2 = convert_to_mark_list(correct_ans)

    assert(len(l1) == len(l2))

    mis = 0  # Missing splits
    uny = 0  # Unnecessary splits
    for i in range(len(l1)):
        if l2[i] == 's' and l1[i] == 'b':
            mis += 1
        elif l2[i] == 'b' and l1[i] == 's':
            uny += 1

    return mis, uny

if __name__ == '__main__':
    test()