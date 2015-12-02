"""Code responsible for GUI interface"""
import tkinter as tk
from Controller import *


class MainView:
    def __init__(self):
        self.r = tk.Tk()
        self.f = tk.Frame()
        self.s = tk.StringVar()
        self.s.set("请输入！")
        self.e = tk.Entry(self.r, textvariable=self.s)
        self.b = tk.Button(self.r, text="Button")
        self.b.configure(command=lambda: self.show_data(MainController.get_segmentation()))

    def show_data(self, data):
        self.s.set(data)

    def add_event(self):
        """Add event here"""
        pass

    def show(self):
        """Show the GUI interface"""
        self.e.pack()
        self.b.pack()
        self.r.mainloop()
