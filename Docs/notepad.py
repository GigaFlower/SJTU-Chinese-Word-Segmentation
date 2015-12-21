"""
A notepad demo
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os


class Notepad:
    def __init__(self):

        self.root = Tk()
        self.root.title("Untitled")

        self.cur_file_name = ""
        self.theme_colors = {'Default': 'Black.White', 'Great Gery': 'Gray.Alice Blue',
                             'Lovely Lavender': '#202B4B.#E1E1FF', 'Aquamarine': '#5B8340.#D1E7E0',
                             'Bold Beige': '#4B4620.#FFF0E1', 'Olive Green': '#D1E7E0.#5B8340'}

        self.shortcut_bar = Frame()
        self.linenum_bar = Label()
        self.info_bar = Label()
        self.text_pad = Text()

        #  settings
        self.show_ln_num = BooleanVar(value=True)  # show line number
        self.hl_cur_ln = BooleanVar(value=False)  # highlight current line
        self.show_info_bar = BooleanVar(value=True)  # highlight current line
        self.theme = StringVar(value="Default")

        self.make_shortcut_bar()
        self.make_linenum_bar()
        self.make_text_pad()
        self.make_info_bar()
        self.make_menu()
        self.update()

        Button(text="123", command=lambda: print(self.theme.get())).pack()

    def run(self):
        self.text_pad.focus()
        self.root.mainloop()

    # Text and scrollbar
    def make_text_pad(self):
        self.text_pad = Text(self.root, undo=True)
        self.text_pad.pack(expand=True, fill=BOTH)
        scroll = Scrollbar(self.text_pad)

        self.text_pad.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.text_pad.yview)
        scroll.pack(side=RIGHT, fill=Y)

    def make_shortcut_bar(self):
        self.shortcut_bar = Frame(self.root, height=25, bg='LightSeaGreen', width=800)

        # icons = ['new', 'open', 'save', 'cut', 'paste', 'redo', 'undo']
        #
        # for ind, ico in enumerate(icons):
        #     img = PhotoImage(file='icons/' + ico + '.gif')
        #     cmd = eval('self.' + ico)

            # Buttons will not show any image until you tell them twice
            # b = Button(self.shortcut_bar, image=img, command=cmd)
            # b.image = img
            # b.pack(side=LEFT, padx=10, pady=5)

        self.shortcut_bar.pack(side=TOP, fill=X)

    def make_linenum_bar(self):
        self.linenum_bar = Label(self.root, width=2, bg='OldLace', height=30)
        self.linenum_bar.pack(side=LEFT, fill=Y)
        self.text_pad.bind_all('<Any-KeyPress>', self.update)

    def make_info_bar(self):
        self.info_bar = Label(self.text_pad, text="Line:1 | Column:0")
        self.info_bar.pack(anchor=SE)

    def make_menu(self):
        # Menus
        # -----------------------------------------------------------
        main_menu = Menu(self.root)

        # file_menu
        file_menu = Menu(main_menu)
        file_menu.add_command(label="New", accelerator="Control+N", command=self.new)
        file_menu.add_command(label="Open", accelerator="Control+O", command=self.open)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Control+S", command=self.save)
        file_menu.add_command(label="Save As", accelerator="Shift+Control+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Control+Q", command=self.exit_editor)

        # edit_menu
        edit_menu = Menu(main_menu)
        edit_menu.add_command(label="Undo", accelerator='Command+Z', command=self.undo)
        edit_menu.add_command(label="Redo", accelerator='Command+Y', command=self.redo)
        edit_menu.add_command(label="Clear", command=self.clear)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator='Command+X', command=self.cut)
        edit_menu.add_command(label="Copy", accelerator='Command+C', command=self.copy)
        edit_menu.add_command(label="Paste", accelerator='Command+V', command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator='Command+A', command=self.select_all)
        edit_menu.add_command(label="Find All", accelerator='Control+F', command=self.on_find)

        # view_menu
        view_menu = Menu(main_menu)
        view_menu.add_checkbutton(label="Show Line Number", variable=self.show_ln_num, command=self.update_linenum)
        view_menu.add_checkbutton(label="Highlight Current Line", variable=self.hl_cur_ln, command=self.update_highlight)
        view_menu.add_checkbutton(label="Show infobar", variable=self.show_info_bar, command=self.update_infobar)

        # theme_menu
        theme_menu = Menu(main_menu)
        for name in sorted(self.theme_colors):
            theme_menu.add_radiobutton(label=name, variable=self.theme, command=self.update_theme)

        # about_menu
        about_menu = Menu(main_menu)
        about_menu.add_command(label="About", command=self.about)
        about_menu.add_command(label="Help", accelerator='F1', command=self.help)

        # menu relationship
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Edit", menu=edit_menu)
        main_menu.add_cascade(label="View", menu=view_menu)
        main_menu.add_cascade(label="About", menu=about_menu)

        self.root.configure(menu=main_menu)

    # Menu button callbacks
    # --------------------------------------------------------------------
    def cut(self):
        self.text_pad.event_generate("<<Cut>>")
        self.update()

    def copy(self):
        self.text_pad.event_generate("<<Copy>>")
        self.update()

    def paste(self):
        self.text_pad.event_generate("<<Paste>>")
        self.update()

    def undo(self):
        self.text_pad.event_generate("<<Undo>>")
        self.update()

    def redo(self):
        self.text_pad.event_generate("<<Redo>>")
        self.update()

    def clear(self):
        self.text_pad.delete('0.0', END)
        self.update()

    def select_all(self):
        self.text_pad.tag_add('sel', '1.0', END)

    def on_find(self):
        t = Toplevel(self.root)
        t.title("Find")

        t.transient(self.root)
        # This makes the window always be in front of the root,even if you click back the root window

        Label(t, text="Find All:").grid(row=0, column=0)

        # target entry
        target = StringVar()
        e = Entry(t, width=25, textvariable=target)
        e.grid(row=0, column=1, columnspan=2, padx=2, pady=2)
        e.focus_set()

        # Case sensitive checkbutton
        c = BooleanVar()
        Checkbutton(t, text='No Cases', variable=c).grid(row=1, column=1, padx=2, pady=2)

        # 'Go' button
        def find():
            t.title("Found %d" % self.find_all(target.get(), c.get()))
            e.focus_set()
        Button(t, text=" Go! ", command=find).grid(row=1, column=2)

        # We should override the close function in order to eliminate the colored tags
        def close_find():
            self.text_pad.tag_remove('match', '1.0', END)
            t.destroy()
        t.protocol('WM_DELETE_WINDOW', close_find)

    def find_all(self, target: str, no_case=False) -> int:
        """This function highlight all target in self.text_pad, returns the count"""
        tp = self.text_pad
        tp.tag_configure('match', foreground='red', background='yellow')
        tp.tag_remove('match', '1.0', END)
        count = 0
        # if target:
        pos = '1.0'
        while True:
            # search function is given by tkinter
            pos = tp.search(target, pos, END, nocase=no_case)
            if not pos:
                break
            lastpos = '%s+%dc' % (pos, len(target))
            tp.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
        return count

    def new(self):
        self.root.title("Untitled")
        self.cur_file_name = ""
        self.text_pad.delete('1.0', END)
        self.update()

    def open(self):
        fname = filedialog.LoadFileDialog(self.root, "Open").go()
        if fname:
            self.text_pad.delete('1.0', END)
            f = open(fname, 'r')
            self.text_pad.insert('1.0', f.read())
            f.close()
            self.root.title(os.path.basename(fname) + "- notepad")
        self.cur_file_name = fname
        self.update()

    def save(self):
        context = self.text_pad.get('1.0', END)
        try:
            f = open(self.cur_file_name, 'w')
            f.write(context)
            f.close()
        except IOError:
            self.save_as()

    def save_as(self):
        fname = filedialog.SaveFileDialog(self.root, "Save").go()
        if fname:
            f = open(fname, "w")
            context = self.text_pad.get('1.0', END)
            f.write(context)
            f.close()
            self.root.title(os.path.basename(fname) + " -notepad")
        self.cur_file_name = fname

    def exit_editor(self):
        if messagebox.askyesno("Exit", "Do you want to you exit?"):
            self.root.destroy()

    def about(self):
        abt = "This notepad programme\nis written for tkinter practice"
        messagebox.showinfo("About", abt)

    def help(self):
        hlp = "You can get source code in notepad.py,\nif you find it difficult to understand.\nGO FUCK YOURSELF"
        messagebox.showinfo("Help", hlp)

    def update(self, e=None):
        self.update_linenum()
        self.update_highlight()
        self.update_infobar()

    def update_linenum(self):
        linenum = ""
        if self.show_ln_num.get():
            endline, _ = self.text_pad.index('end+1c').split('.')
            linenum = "\n".join(map(str, range(1, int(endline))))

        self.linenum_bar.configure(text=linenum, anchor=N)

    def update_highlight(self):
        self.text_pad.tag_delete('cur_line')
        if self.hl_cur_ln.get():
            self.text_pad.tag_add('cur_line', 'insert linestart', 'insert lineend+1c')
            self.text_pad.tag_configure('cur_line', background='yellow')

    def update_infobar(self):
        if self.show_info_bar.get():
            self.info_bar.pack(side=BOTTOM, anchor=SE)
            x, y = self.text_pad.index('insert').split(".")
            self.info_bar.configure(text='Line:%s | Column:%s' % (x, y))
        else:
            self.info_bar.pack_forget()

    def update_theme(self):
        color = self.theme_colors.get(self.theme.get(), 'Black.White')
        fore, back = color.split('.')
        self.text_pad.configure(foreground=fore, background=back)

if __name__ == '__main__':
    n = Notepad()
    n.run()

