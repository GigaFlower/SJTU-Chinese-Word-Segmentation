"""
This file test the accuracy and efficiency of segmentation
Test corpus comes from ShanXi University
"""
import kernel
import re,time

SPLIT = '|'


def record_time(method):
    def new_method(*args):
        t0 = time.time()
        method(*args)
        print(time.time()-t0)
    return new_method


@record_time
def test(amount=20):
    seg = kernel.Segmentation()

    src_file = open('test.txt', 'r')
    ans_file = open('answer.txt', 'r')

    cnt = 0
    wrong_cnt = 0

    for line in src_file:
        cnt += 1
        if cnt > amount:
            break

        ans = ans_file.readline()
        ans = re.sub(r'\s+', SPLIT, ans)

        # ret = seg.word_segment(line)
        ret = '123'
        
        if ans == ret:
            print('Sentence #%d passed!' % cnt)
        else:
            wrong_cnt += 1
            print('Sentence #%d failed!' % cnt)
            print('Correct answer:')
            print(ans)
            print('Your answer:')
            print(ret)

    print('All %d tests done.' % cnt)
    print('%d tests failed' % wrong_cnt)
    print('Precision:%.2f%%' % (1-wrong_cnt/cnt))


if __name__ == '__main__':
    test()