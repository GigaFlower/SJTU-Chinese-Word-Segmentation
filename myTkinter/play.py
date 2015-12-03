# import tkinter as tk
# from demo_geo_man import *
# from demo_event import *
from demo_widgets import *


def example():
    root = tk.Tk()

    tk.Label(root, text="查找:").grid(row=0, column=0, sticky='w')
    tk.Label(root, text="替换为:").grid(row=1, column=0, sticky='w')
    tk.Entry(root, width=40).grid(row=0, column=1, columnspan=2)
    tk.Entry(root, width=40).grid(row=1, column=1, columnspan=2)

    tk.Checkbutton(root, text="全字匹配").grid(row=2, column=1, sticky='w')
    tk.Checkbutton(root, text="区分大小写").grid(row=3, column=1, sticky='w')
    tk.Checkbutton(root, text="高亮所有").grid(row=4, column=1, sticky='w')

    tk.Label(root, text='方向').grid(row=2, column=2, sticky='w')
    tk.Radiobutton(root, text='朝上', value=1).grid(row=3, column=2, sticky='w')
    tk.Radiobutton(root, text='朝下', value=2).grid(row=4, column=2, sticky='w')

    tk.Button(root, text='查找', width=8).grid(row=0, column=4, padx=10)
    tk.Button(root, text='查找所有', width=8).grid(row=1, column=4, padx=10)
    tk.Button(root, text='替换', width=8).grid(row=2, column=4, padx=10)
    tk.Button(root, text='替换所有', width=8).grid(row=3, column=4, padx=10)

    root.columnconfigure(1, weight=2)
    root.columnconfigure(2, weight=3)

    root.mainloop()


def play_around():
    root = tk.Tk()

    for bdw in range(5):
        column = tk.Frame(root, borderwidth=1, relief='groove')
        tk.Label(column, text="borderwidth:%d" % bdw).pack(side="left")
        for rel in ["raised", "sunken", "flat", "ridge", "groove", "solid"]:
            f = tk.Frame(column, borderwidth=bdw, relief=rel)
            tk.Label(f, text=rel).pack()
            f.pack(side="left", padx=5, pady=5)
        column.pack(expand=True, fill="x")

    root.mainloop()


if __name__ == '__main__':

    root = tk.Tk()

    a = tk.Label(root, text="123")
    b = tk.Label(root, text="456")
    a.pack()
    b.pack()

    root.mainloop()
