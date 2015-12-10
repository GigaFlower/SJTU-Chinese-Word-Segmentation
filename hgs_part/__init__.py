"""
Code responsible for service logic
"""


class Segmentation:
    def __init__(self):
        self.lex = Lexicon("lexicon.txt")
        pass

    def sentence_segment(self, raw: str) -> str:
        return "%s(已分句)" % raw

    def word_segment(self, raw: str) -> str:

        return "%s(已分词)" % raw


class Lexicon:
    def __init__(self, filename):
        self.lex = []
        src = open(filename, "r").read()
        self.lex = src.split()

