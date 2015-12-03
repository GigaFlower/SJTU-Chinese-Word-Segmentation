"""
此处是tkinter主要控件的演示程序。
也将涉及tkinter特有的变量类型相关的内容
简而言之，tkinter提供了由传统int，str类型拓展而来的类型来控制控件相关的变量。
例如一个输入框的内容是tk.StringVar类型而不是str类型
"""

import tkinter as tk


def demo_label_button():
    """Label和Button是最基础的控件之一，Label用于显示文本，Button用于响应时间
    但你也可以为Label控件绑定事件，使之成为一个“cheap”的Button
    """
    root = tk.Tk()
    root.minsize(300, 300)
    tk.Label(text="A label", borderwidth=1, relief='solid').pack(pady=10)
    tk.Button(text="A Button").pack(pady=10)
    root.mainloop()


def demo_frame():
    """Frame 是一种容器控件，其主要作用是集合别的控件，以方便排版或区分不同功能的控件"""
    root = tk.Tk()

    for rel in ["raised", "sunken", "flat", "ridge", "groove", "solid"]:
        f = tk.Frame(root, borderwidth=2, relief=rel)
        tk.Label(f, text=rel).pack()
        f.pack(side="left", padx=5, pady=5)

    root.mainloop()


def demo_entry():
    """Entry是输入文本框，用于接收文本输入"""
    root = tk.Tk()

    tk.Label(text="这是个文本框：").pack(padx=5, pady=5)
    s = tk.StringVar()
    tk.Entry(root, textvariable=s).pack()
    s.set("请随意输入")

    root.mainloop()


def demo_radiobutton():
    """单选按钮,通过绑定同一个变量来实现“单选"""
    root = tk.Tk()

    var = tk.IntVar()
    for t, v in [("dog", 1), ("cat", 2), ("fish", 3), ("bird", 4), ("elephant", 5), ("ant", 6)]:
        tk.Radiobutton(root, text=t, value=v, variable=var).pack(anchor='w')

    root.mainloop()


def demo_menu():
    root = tk.Tk()

    tk.m
    root.mainloop()