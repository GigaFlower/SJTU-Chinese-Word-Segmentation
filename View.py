"""Code responsible for GUI interface"""
import tkinter as tk
from Controller import *


class MainView:
    def __init__(self):
        pass

    @staticmethod
    def show():
        """Show the GUI interface"""
        m = MainController()
        root = tk.Tk()
        e = tk.Entry(root)
        e.pack()

        tk.Button(root, text="Button", command=lambda: m.do_segmentation(e.get())).pack()
        root.mainloop()
