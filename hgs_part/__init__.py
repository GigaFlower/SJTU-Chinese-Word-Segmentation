"""
Code responsible for service logic
"""


class Segmentation:
    """This class handles all staff relating to segmentation"""
    def __init__(self):
        # Initialize lexicon
        self.lex = Lexicon("lexicon.txt")

        # Initialize rules
        self.rules = Rule()

    def sentence_segment(self, raw: str) -> str:
        return "%s(已分句)" % raw

    def word_segment(self, raw: str) -> str:
        return "%s(已分词)" % raw


class Lexicon:
    """This class represents a lexicon library"""
    def __init__(self, filename):
        """Load a lexicon from a txt file"""
        self.lex = []
        src = open(filename, "r").read()
        self.lex = src.split()


class Rule:
    """This class represents a rule library"""
    pass
