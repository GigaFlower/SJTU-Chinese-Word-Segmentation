"""
Code responsible for service logic
All the function this file should realize is word-segmentation
"""


class Segmentation:
    def __init__(self):
        self.lex = Lexicon("lexicon.txt")

    def sentence_segment(self, raw: str) -> str:
        return "%s(已分句)" % raw

    def word_segment(self, raw: str) -> str:
        return "%s(已分词)" % raw


class Lexicon:
    def __init__(self, filename):
        self.lex = []

        try:
            src = open(filename, "r").read()
        except FileNotFoundError:
            src = ""

        self.lex = src.split()

