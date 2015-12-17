from tkinter import *


class Demo:
    def __init__(self, root):
        self.root = root

        Frame(root, bg='LightSeaGreen', width=800, height=25).pack(side=TOP, fill=X)

        Label(root, bg='Beige', width=2, height=30).pack(side=LEFT, fill=Y)

        self.text_pad = Text(root)
        self.text_pad.pack(expand=True, fill=BOTH)

        s = Scrollbar(self.text_pad)
        self.text_pad.configure(yscrollcommand=s.set)
        s.configure(command=self.text_pad.yview)
        s.pack(side=RIGHT, fill=Y)

        self.make_menu()

        self.text_pad.bind_all('<Any-KeyPress>', self.highlight)

    def run(self):
        self.root.mainloop()

    def make_menu(self):
        """This function makes menus"""
        main_menu = Menu(self.root)
        file_menu = Menu(main_menu)
        file_menu.add_command(label="1", accelerator='Shift+A')
        file_menu.add_command(label="3", accelerator='Shift+B')
        file_menu.add_separator()
        file_menu.add_command(label="5", accelerator='Shift+C')
        file_menu.add_command(label="7", accelerator='Shift+D')

        edit_menu = Menu(main_menu)
        edit_menu.add_command(label="2", accelerator='Ctrl+A')
        edit_menu.add_command(label="4", accelerator='Ctrl+A')
        edit_menu.add_command(label="6", accelerator='Ctrl+A')
        edit_menu.add_command(label="8", accelerator='Ctrl+A')

        main_menu.add_cascade(label='胡萝卜', menu=file_menu)
        main_menu.add_cascade(label='西红柿', menu=edit_menu)

        root.configure(menu=main_menu)

    def highlight(self, event):
        self.text_pad.tag_delete('cur_line')
        self.text_pad.tag_add('cur_line', 'insert linestart', 'insert lineend')
        self.text_pad.tag_configure('cur_line', background='yellow')

root = Tk()
d = Demo(root)
d.run()