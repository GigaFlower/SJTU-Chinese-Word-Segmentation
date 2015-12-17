"""Code responsible for GUI interface"""
from tkinter import *


class DemoView:
    def __init__(self, master: Tk):
        # Root window
        self.root = master

        # Three main text pads
        self.raw_text_pad = Text()
        self.sen_text_pad = Listbox()
        self.wrd_text_pad = Text()

        self.set_text_pad()
        self.make_button()

    def run(self):
        self.root.mainloop()

    def set_text_pad(self):
        """
        This function setting the properties of
        raw_text_pad.sen_text_pad and wrd_text_pad
        """
        # setting raw_text_pad
        self.raw_text_pad = Text(self.root)

        # setting sen_text_pad
        self.sen_text_pad = Listbox(self.root)

        # setting wrd_text_pad
        self.wrd_text_pad = Text(self.root)

    def make_button(self):
        # Buttons
        btn1 = Button(self.root, text="分词")
        btn2 = Button(self.root, text="分句")
        btn3 = Button(self.root, text="打开文件")

        btn1.configure(command=self.__sen_seg)
        btn2.configure(command=self.__wrd_seg)
        btn3.configure(command=self.__read_file)

        # btn1.pack(side='left', expand=True)
        # btn2.pack(side='left', expand=True)
        # btn3.pack(side='left', expand=True)

    # Following functions involves conversation with controller
    def register(self, controller):
        """Make connection with controller"""
        self.controller = controller

    def __sen_seg(self):
        # Get the unprocessed variable
        before = self.raw_text_pad.get('1.0', END)

        # Get the sentence-segmentation function provided by controller
        seg = self.controller.sentence_segment
        # Do sentence segmentation
        after = seg(before)
        # Renew variable
        self.sen_text_pad.insert('end', after)

    def __wrd_seg(self):
        seg = self.controller.word_segment
        after_wrd_seg = seg(self.sen_text_pad.get('1.0', END))
        self.wrd_text_pad.insert('1.0', END, after_wrd_seg)

    def __read_file(self):
        s = self.raw_text_pad.get('1.0', END)
        s.set(self.controller.read_file(s.get()))


if __name__ == '__main__':
    root = Tk()
    t = DemoView(root)
    t.run()