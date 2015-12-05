"""Code responsible for application logic"""
import tkinter as tk
from View import TestView
import Model


class MainController:
    """The main controller of app activity"""
    def __init__(self):
        self.root = tk.Tk()
        self.view = TestView(self.root)
        self.view.register(self)
        self.model = Model.Segmentation()

    def run(self):
        self.view.show()
        self.root.mainloop()

    def sentence_segment(self, raw: str) -> str:
        return self.model.sentence_segment(raw)

    def word_segment(self, sentence: str) -> str:
        return self.model.word_segment(sentence)

