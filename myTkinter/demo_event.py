"""
此处是tkinter事件响应的演示程序

所谓事件是指窗口内的控件与用户交互的一种方式
包括点击、双击、键盘输入等
而事件响应就是指对这些事件做出回应
"""

import tkinter as tk

##################################################
# 响应事件的第一种方式：Command Binding
# 注:只有Button可以使用这种方式，当单击或空格时触发
##################################################


def demo_cmd_binding_1():
    """Basic usage of command binding"""
    # 所谓Command binding是指在Button初始化时设置其command参数为点击时要触发的函数
    # 一经设置，无法修改
    # 注意是赋给command的是函数本身，而不是返回值，所以没有括号！（如果有括号，那是函数的返回值，没有括号，代表函数）

    def my_call_back():
        print("I'm called!")

    root = tk.Tk()
    root.title("Command binding")
    root.minsize(300, 300)
    tk.Button(root, text="Click me!", command=my_call_back).pack()
    root.mainloop()


def demo_cmd_binding_2():
    """Command binding in lambda manner"""
    # 以匿名函数方法实现的Command binding

    root = tk.Tk()
    root.title("Command binding with lambda")
    root.minsize(300, 300)
    tk.Button(root, text="Click me!", command=lambda: print("I'm called!")).pack()
    root.mainloop()


##################################################
# 响应事件的第二种方式：Event Binding
# 真正自由定制响应事件的方式
##################################################


def demo_event_1():
    """Basic usage of event"""
    # 利用widget的bind函数来进行事件的绑定
    # bind函数接收两个参数，第一个是描述事件的字符串，第二个是事件发生时触发的函数
    # 当与描述字符串相符的事件发生时，一个Event对象将作为参数传给响应的函数，该对象的属性包括事件发生时的鼠标位置，键盘值等等
    # 描述字符串的例子：<Button-1>鼠标左击 <Double-Button-1>双击 <KeyPress-A> 键盘A,更多见文档
    # 注意别忘了尖括号！

    root = tk.Tk()
    root.title("Demo of event")
    root.minsize(300, 300)
    mylabel = tk.Label(root, text="Click at the different\nlocations in the frame below!")
    mylabel.pack()

    def my_callback(event):
        mylabel.configure(text="You clicked at (%d,%d)" % (event.x, event.y))

    myframe = tk.Frame(root, bg='Yellow', width=200, height=200)
    myframe.bind("<Button-1>", my_callback)
    myframe.pack()
    root.mainloop()


def demo_event_2():
    """Levels of binding levels"""
    # 当使用bind_all函数时，所有的widget都被绑定事件，称为“Application level binding”
    # 当使用bind_class函数时，所有的指定class的widget都被绑定事件,称为“Class level binding"

    root = tk.Tk()
    root.title("Demo of event")
    root.minsize(300, 300)
    mylabel = tk.Label(root, text="Click at the different locations in any frame!")
    mylabel.grid(row=0, column=0, columnspan=2)

    def my_callback(event):
        mylabel.configure(text="You clicked at (%d,%d)" % (event.x, event.y))

    # 生成四个不同颜色的frame
    colors = ['Yellow', 'Pink', 'LightCyan', 'SteelBlue']
    myframes = [tk.Frame(root, bg=col, width=200, height=200) for col in colors]
    myframes[0].grid(row=1, column=0)
    myframes[1].grid(row=1, column=1)
    myframes[2].grid(row=2, column=0)
    myframes[3].grid(row=2, column=1)

    # 生成四个Button
    for i in range(4):
        tk.Button(root, text="%d" % i, width=20).grid(row=3+i//2, column=i % 2)

    # 所有widget被点击时都会显示点击坐标
    # 但只有button被点击时，会在控制台输出信息
    root.bind_all("<Button-1>", my_callback)
    root.bind_class("Button", "<Button-1>", lambda event: print("I'm clicked!"))
    root.mainloop()