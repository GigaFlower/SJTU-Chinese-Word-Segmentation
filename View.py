"""Code responsible for GUI interface"""
import tkinter as tk


class TestView:
    def __init__(self, master: tk.Tk):
        # Root window
        self.root = master
        self.root.minsize(300, 300)

        # Core string variables
        self.raw_str = tk.StringVar()
        self.raw_str.set("请输入！")
        self.sen_str = tk.StringVar()
        self.wrd_str = tk.StringVar()

        # Entries
        self.ety1 = tk.Entry(self.root, textvariable=self.raw_str)
        self.ety2 = tk.Entry(self.root, textvariable=self.sen_str)
        self.ety3 = tk.Entry(self.root, textvariable=self.wrd_str)

        self.ety1.pack()
        self.ety2.pack()
        self.ety3.pack()

        # Buttons
        self.btn1 = tk.Button(self.root, text="分词")
        self.btn2 = tk.Button(self.root, text="分句")
        self.btn3 = tk.Button(self.root, text="打开文件")

        self.btn1.configure(command=self.__sen_seg)
        self.btn2.configure(command=self.__wrd_seg)
        self.btn3.configure(command=self.__read_file)

        self.btn1.pack(side='left', expand=True)
        self.btn2.pack(side='left', expand=True)
        self.btn3.pack(side='left', expand=True)

    # Following functions involves conversation with controller
    def register(self, controller):
        """Make connection with controller"""
        self.controller = controller

    def __sen_seg(self):
        # Get the unprocessed variable
        before = self.raw_str.get()

        # Get the sentence-segmentation function provided by controller
        seg = self.controller.sentence_segment
        # Do sentence segmentation
        after = seg(before)
        # Renew variable
        self.sen_str.set(after)

    def __wrd_seg(self):
        seg = self.controller.word_segment
        after_wrd_seg = seg(self.sen_str.get())
        self.wrd_str.set(after_wrd_seg)

    def __read_file(self):
        s = self.raw_str
        s.set(self.controller.read_file(s.get()))
