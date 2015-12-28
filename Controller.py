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
        ask Model to do word segmentation,
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
        return sorted(lex[0].keys())

    def get_term(self) -> list:
        """
        Get terms from self.kernel
        """
        lex = self.kernel.get_lexicon()
        return sorted(lex[1].keys())

    def get_rule_description(self) -> list:
        """Get rules from self.kernel"""
        return self.kernel.get_rule_description()

    def set_rule_booleans(self, bools):
        """Tell self.kernel which rule need to be obeyed"""
        self.kernel.set_rule_boolean(bools)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
