"""
此处是tk图形管理器（Geometry Manager）的演示程序。

每个widget都必须有一种图形管理器来管理，否则空有数据，却无法显示。
在tk中共有三种图形管理器：pack、grid、place

用法： SomeWidget.<Geometry Manager>(paras)
e.g.
tk.Button(root).pack(side='top')
tk.Label(root).grid(row)
"""

import tkinter as tk

##################################################
# pack的演示程序
# pack的主要参数：side、fill、expand、anchor
##################################################


def demo_pack_1():
    """Show the effect of para 'side'"""
    # Valid value:'top', 'bottom', 'left', 'right'

    root = tk.Tk()
    root.title('demo of pack(side)')
    root.minsize(200, 200)
    sides = ['top', 'bottom', 'left', 'right']
    for a in sides:
        tk.Button(root, text=a).pack(side=a)
    root.mainloop()


def demo_pack_2():
    """Show the effect of para 'fill'"""
    # Valid value:'x','y','both'

    root = tk.Tk()
    root.title('Stretch me to show the effect!')
    root.minsize(200, 200)
    tk.Button(root, text='I fill in x!').pack(fill='x')
    tk.Button(root, text='I fill in y!').pack(expand=True, fill='y')
    root.mainloop()


def demo_pack_3():
    """
    Show the effect of para 'expand'"""
    # Valid value:True,False

    # 展示expand参数的效果
    # 注意！expand仅改变widget是否尽量占据空间，而不改变其显示大小，若想同时改变两者，结合使用fill参数
    # 应用expand的控件将等分窗口高度
    root = tk.Tk()
    root.title('Stretch me to show the effect!')
    root.minsize(200, 600)
    tk.Button(root, text='I expand in x!').pack(expand=True, fill='x')
    tk.Button(root, text='I expand in x but I do not fill in x!').pack(expand=True)
    tk.Button(root, text='I expand in y!').pack(expand=True, fill='y')
    tk.Button(root, text='I expand in both directs!').pack(expand=True, fill='both')
    tk.Button(root, text='I do not expand T_T!').pack(expand=False)
    root.mainloop()


def demo_pack_4():
    """Show the effect of 'anchor'"""
    # Valid value:'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'
    # anchor 参数决定widget在它所占据的空间中的位置

    root = tk.Tk()
    root.title('Stretch me to show the effect!')
    root.minsize(200, 600)
    anchors = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']
    for a in anchors:
        tk.Button(root, text='anchor:%s' % a).pack(expand=True, anchor=a)
    root.mainloop()
##################################################
# 总结:当你需要控件撑满其容器时，使用pack
##################################################


##################################################
# grid:使用假想的表格来定位控件
# 每个单元格的大小由其内容决定
# 主要参数:row, column, sticky
##################################################

def demo_grid_1():
    """Show the effect of para 'row' and 'column'"""
    # Valid value:Int

    root = tk.Tk()
    root.title('A 5*5 grid!')
    for i in range(5):
        for j in range(5):
            tk.Button(root, text=chr(ord('a')+i*5+j)).grid(row=i, column=j)
    root.mainloop()


def demo_grid_2():
    """Show the self-adaption"""
    #当单元格的大小不同时，其同行同列的单元格将调节自己的大小以适应

    root = tk.Tk()
    root.title('Self-adaption!')
    for i in range(5):
        for j in range(5):
            if (i, j) == (4, 4):
                tk.Entry(root).grid(row=i, column=j)
            else:
                tk.Button(root, text=chr(ord('a')+i*5+j)).grid(row=i, column=j)
    root.mainloop()


def demo_grid_3():
    """Show the effect of para 'sticky"""
    # Valid value:'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'
    # 当单元格比格内容大时，sticky决定它靠向哪一边

    root = tk.Tk()
    root.title("Demo of 'sticky'")
    sticky = [None, 'w', 'e']
    for i in range(3):
        for j in range(3):
            if i == j:
                tk.Entry(root).grid(row=i, column=j)
            else:
                tk.Button(root, text="sticky='%s'" % sticky[j]).grid(row=i, column=j, sticky=sticky[j])
    root.mainloop()


def demo_grid_4():
    """Show the effect of para 'rowspan' and 'columnspan'"""
    # Valid value:Int
    # rowspan 和 columnspan使得widget可以占据多个单元格

    root = tk.Tk()
    root.title('A spanning grid!')
    for i in range(5):
        for j in range(5):
            tk.Button(root, text="(%d,%d)" % (i,j)).grid(row=i, column=j)
    tk.Button(root, text='rowspan\n=2').grid(row=0, column=0, rowspan=2)
    tk.Button(root, text='columnspan=2').grid(row=4, column=3, columnspan=2)
    tk.Button(root, text='rowspan=2\ncolumnspan=3').grid(row=2,column=1, rowspan=2, columnspan=3)

    root.mainloop()


def demo_grid_5():
    """Show the usage of function rowconfigure() and columnconfigure()"""
    # rowconfigure() and columnconfigure()方法使得我们可以在单元格生成后改变它的属性
    # 可选参数：minsize、pad、weight
    root = tk.Tk()
    root.title('Demo of configure()')
    for i in range(5):
        for j in range(5):
            if i == 4 and j >= 3:
                continue
            tk.Button(root, text=chr(ord('a')+i*5+j)).grid(row=i, column=j, sticky='e')
    tk.Entry(root).grid(row=4, column=3, columnspan=2)

    root.columnconfigure(3, weight=2)
    root.columnconfigure(4, weight=3)
    # 使得四五列宽度比为2:3
    root.columnconfigure(0, pad=10)
    # 为第一列添加10pad
    root.mainloop()

##################################################
# 总结:最好用的Geometry Manager，首选使用
##################################################

##################################################
# place:为每个控件提供基于坐标的定位
# 主要参数:x,y,relx,rely,width,height,relwidth,relheight
##################################################


def demo_place_1():
    """Show the basic usage"""

    root = tk.Tk()
    root.title("Demo of 'place'")
    tk.Button(root, text="x=2, y=2").place(x=2, y=2)
    tk.Button(root, text="x=3, y=20").place(x=3, y=20)
    tk.Button(root, text="x=0, y=80\nheight=100, width=170").place(x=0, y=80, height=100, width=170)
    root.mainloop()


def demo_place_2():
    """Show the usage of para 'rel-XXX'"""
    # 使用rel来进行相对定位

    root = tk.Tk()
    root.title("Stretch me!")
    tk.Button(root, text="Absolute").place(x=0, y=0)
    tk.Button(root, text="我永远保持在距顶20%处").place(rely=0.2)
    tk.Button(root, text="我永远保持\n窗体50%的宽\n与30%的高度").place(relx=0.3,rely=0.5,relwidth=0.5,relheight=0.3)
    root.mainloop()

##################################################
# 总结:最少使用的Geometry Manager,但只有place可以和别的Manager结合使用
##################################################
