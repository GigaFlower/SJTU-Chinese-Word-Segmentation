"""Code responsible for application logic"""

import View
import kernel


class MainController:
    """The main controller of app activity"""
    def __init__(self):
        self.kernel = kernel.Segmentation()
        self.view = View.DemoView(self)

    def run(self):
        self.view.run()

    @staticmethod
    def read_file(filename: str) -> str:
        """
        This function opens a file according to its name,and return its context.
        If can't open with 'utf-8',try 'gbk',
        since 'gbk' always opens a file even if open it as error codes

        Questions:
        1.Error message should not be only print!
        2.Not tested yet
        """

        context = ""
        try:
            with open(filename, "r", encoding='utf') as f:
                context = f.read()
        except IOError:
            print("Can't find file!")
        except UnicodeDecodeError:
            with open(filename, "r", encoding='gbk') as f:
                context = f.read()
        return context

    def sentence_segment(self, raw: str) -> list:
        """
        This function receive complete long string from View,
        ask for Model to do sentence segmentation,
        return processed string list to View.

        Only called by View.

        Examples:
        >>> c = MainController()
        >>> c.sentence_segment("你好，再见。")
        ['你好，', '再见。']

        """
        aft_seg = self.kernel.sentence_segment(raw)
        aft_seg = [x for x in aft_seg if x.strip()]
        return aft_seg

    def word_segment(self, sentence: str) -> str:
        """
        This function receive a sentence from View,
        ask for Model to do word segmentation,
        return processed string to View.

        Only called by View.

        Examples:
        >>> c = MainController()
        >>> c.word_segment("我喜欢足球")
        '我|喜欢|足球'
        """
        return self.kernel.word_segment(sentence)

    def get_lexicon(self) -> list:
        """
        Get lexicon from self.kernel
        According to self.kernel,we get a bi-tuple containing a dict in the of 'XXX':XXX and a dict of 'XXX':['TERM']
        like ({'姑娘':25686900,...},{'五大三粗':['TERM']...})
        """
        lex = self.kernel.get_lexicon()
        return lex[0].keys()

    def get_term(self) -> list:
        """
        Get terms from self.kernel
        """
        lex = self.kernel.get_lexicon()
        return lex[1].keys()

    def get_rule_description(self) -> list:
        """Get rules from self.kernel"""
        return self.kernel.get_rule_description()

    def set_rule_booleans(self, bools):
        """Tell self.kernel which rule need to be obeyed"""
        self.kernel.set_rule_boolean(bools)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
