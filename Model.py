"""
Code responsible for service logic
All the function this file should realize is word-segmentation
"""


class Segmentation:
    def __init__(self):
        #self.lex = Lexicon("lexicon.txt")
        pass
    def sentence_segment(self, raw: str) -> str:
        return "%s(宸插垎鍙?" % raw

    def word_segment(self, raw: str) -> str:
        return "%s(宸插垎璇?" % raw


class Lexicon:
    def __init__(self, filename):
        self.lex = []

        try:
            src = open(filename, "r", encoding = "utf-16").read()
        except FileNotFoundError:
            src = ""

        self.lex = src.split()

