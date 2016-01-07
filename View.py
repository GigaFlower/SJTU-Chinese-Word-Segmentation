"""Code responsible for GUI interface"""
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk


class View:
    def __init__(self, controller):
        self.controller = controller
        # Root window
        self.root = Tk()
        self.root.title("Chinese Segmentation Prototype System")

        # Three main text pads
        # Only remind coder that there exist these properties
        # Actual initialization is done in self.make_XXX()
        self.raw_text_pad = Text()
        self.sen_text_pad = Listbox()
        self.wrd_text_pad = Text()

        # The window of setting configuration
        self.setting_window = ttk.Notebook()
        self.setting_window_on = False
        self.setting_tabs = ttk.Notebook()

        # Three pad in the setting window
        self.lexi_pad = Listbox()
        self.term_pad = Listbox()
        self.situ_pad = Listbox()

        # Rule variables
        self.rule_booleans = []
        self.rule_description = []

        # File variables
        self.file_name = ""

    def run(self):
        self.make_text_pad()
        self.make_menu()
        self.root.mainloop()

    def make_menu(self):
        main_menu = Menu(self.root)

        # file_menu
        file_menu = Menu(main_menu)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open)
        file_menu.add_command(label="Open Recent")
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        file_menu.add_command(label="Save As", accelerator="Shift+Ctrl+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export", command=self.export)
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit)

        self.root.bind('<Control-N>', self.new)
        self.root.bind('<Control-O>', self.open)
        self.root.bind('<Control-S>', self.save)
        self.root.bind('<Shift-Control-S>', self.save_as)
        self.root.bind('<Control-Q>', self.exit)

        # edit_menu
        edit_menu = Menu(main_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo", accelerator="Shift+Ctrl+Z", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)

        self.root.bind('<Control-Z>', self.undo)
        self.root.bind('<Shift-Control-Z>', self.redo)
        self.root.bind('<Control-X>', self.cut)
        self.root.bind('<Control-C>', self.copy)
        self.root.bind('<Control-V>', self.paste)
        # FIXME: These accelerators do not apply to Mac system

        # segment_menu
        segment_menu = Menu(main_menu)
        segment_menu.add_command(label="Sentence Segment", command=self.sentence_segment)
        segment_menu.add_command(label="Word Segment", command=self.word_segment)
        segment_menu.add_command(label="Segment all", command=self.segment_all)
        segment_menu.add_command(label="File to file", command=self.file_to_file)
        segment_menu.add_command(label="Clear", accelerator="Shift+Ctrl+C", command=self.clear)

        # data_menu
        data_menu = Menu(main_menu)
        data_menu.add_command(label="Lexicon", command=self.show_lexicon_pane)
        rule_menu = Menu(data_menu)
        rule_menu = self.load_rule_options(rule_menu)
        rule_menu.add_separator()
        rule_menu.add_command(label="Edit", command=self.show_rule_pane)
        data_menu.add_cascade(label="Rules", menu=rule_menu, command=self.show_rule_pane)

        # help_menu
        help_menu = Menu(main_menu)
        help_menu.add_command(label="Help", command=self.help)
        help_menu.add_command(label="About", command=self.about)

        # main_menu
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Edit", menu=edit_menu)
        main_menu.add_cascade(label="Segment", menu=segment_menu)
        main_menu.add_cascade(label="Data", menu=data_menu)
        main_menu.add_cascade(label="Help", menu=help_menu)

        self.root.configure(menu=main_menu)

    def make_text_pad(self):
        """This function setting the properties of raw_text_pad,sen_text_pad and wrd_text_pad"""
        # setting raw_text_pad
        self.raw_text_pad = Text(self.root, width="40", height="40")
        self.raw_text_pad.pack(side=LEFT, fill=Y)

        # setting sen_text_pad
        self.sen_text_pad = Listbox(self.root, width="40", height="40", selectmode=EXTENDED)
        self.sen_text_pad.pack(side=LEFT, fill=Y)

        # setting wrd_text_pad
        self.wrd_text_pad = Text(self.root, width="40", height="40")
        self.wrd_text_pad.pack(side=LEFT, fill=Y)

    def make_setting_pad(self, tab=0):
        """Make setting_pad which is to be triggered from clicking at 'Lexicon' or 'Rule' in menu"""
        self.setting_window = Toplevel()
        self.setting_window.minsize(400, 200)
        self.setting_window.resizable(False, False)

        # Override window delete function
        def delete_setting_window():
            self.setting_window_on = False
            self._set_rules()
            self.setting_window.destroy()
        self.setting_window.protocol('WM_DELETE_WINDOW', delete_setting_window)

        # Make notebook
        self.setting_tabs = ttk.Notebook(self.setting_window)

        # Make lexicon_tab
        lexicon_tab = Frame(self.setting_tabs)
        self.lexi_pad = Listbox(lexicon_tab, selectmode=EXTENDED)
        self.lexi_pad.pack(side=LEFT, fill=Y)
        self.add_scrollbar(self.lexi_pad)

        Button(lexicon_tab, text='Load', width=7, command=self.load_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Add', width=7, command=lambda: self.listbox_add(self.lexi_pad)).pack(expand=True)
        Button(lexicon_tab, text='Search', width=7, command=lambda: self.listbox_find(self.lexi_pad)).pack(expand=True)
        Button(lexicon_tab, text='Delete', width=7, command=lambda: self.listbox_delete(self.lexi_pad)).pack(expand=True)

        # Make term_tab
        # FIXME:This part is almost same as 'make lexicon_tab' above!Combine them!
        term_tab = Frame(self.setting_tabs)
        self.term_pad = Listbox(term_tab, selectmode=EXTENDED)
        self.term_pad.pack(side=LEFT, fill=Y)
        self.add_scrollbar(self.term_pad)

        Label(term_tab, text="Here goes terminologies\nwith highest segmentation priority.").pack()
        Button(term_tab, text='Load', width=7, command=self.load_term).pack(expand=True)
        Button(term_tab, text='Add', width=7, command=lambda: self.listbox_add(self.term_pad)).pack(expand=True)
        Button(term_tab, text='Search', width=7, command=lambda: self.listbox_find(self.term_pad)).pack(expand=True)
        Button(term_tab, text='Delete', width=7, command=lambda: self.listbox_delete(self.term_pad)).pack(expand=True)

        # Make situ_tab

        situ_tab = Frame(self.setting_tabs)
        self.situ_pad = Listbox(situ_tab, selectmode=EXTENDED)
        self.situ_pad.pack(side=LEFT, fill=Y)
        self.add_scrollbar(self.situ_pad)

        Label(situ_tab, text="Here goes special situations\n"
                             "if the specific situation is encountered,\nit will be segmented as shown."
              ).pack()
        Button(situ_tab, text='Load', width=7, command=self.load_situ).pack(expand=True)
        Button(situ_tab, text='Add', width=7, command=lambda: self.listbox_add(self.situ_pad)).pack(expand=True)
        Button(situ_tab, text='Delete', width=7, command=lambda: self.listbox_delete(self.situ_pad)).pack(expand=True)

        #
        self.setting_tabs.add(lexicon_tab, text="Lexicon")
        self.setting_tabs.add(term_tab, text="Terms")
        self.setting_tabs.add(situ_tab, text="Rules")
        self.setting_tabs.select(tab)
        self.setting_tabs.pack(expand=True, fill=BOTH)

    # Menu functions
    # ----------------------------------------------------------
    # File menu functions
    def new(self):
        self.raw_text_pad.delete('1.0', END)

    def open(self):
        f_name = filedialog.askopenfilename()
        if f_name:
            f = open(f_name)
            self.raw_text_pad.delete('1.0', END)
            self.raw_text_pad.insert('1.0', f.read())
            f.close()
            self.file_name = f_name

    def save(self):
        try:
            f = open(self.file_name, 'w')
            f.write(self.raw_text_pad.get('1.0', END))
            f.close()
        except IOError:
            # This means self.file_name is invalid
            self.save_as()

    def save_as(self):
        f_name = filedialog.asksaveasfilename()
        if f_name:
            f = open(f_name, 'w')
            f.write(self.raw_text_pad.get('1.0', END))
            f.close()
            self.file_name = f_name

    def export(self):
        if self.has_wrd:
            f = filedialog.asksaveasfile()
            if f:
                f.write(self.wrd_text_pad.get('1.0', END))
                f.close()

    def exit(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.root.destroy()

    # Edit menu functions
    def undo(self):
        self.raw_text_pad.event_generate("<<Undo>>")

    def redo(self):
        self.raw_text_pad.event_generate("<<Redo>>")

    def cut(self):
        self.raw_text_pad.event_generate("<<Cut>>")

    def copy(self):
        self.raw_text_pad.event_generate("<<Copy>>")

    def paste(self):
        self.raw_text_pad.event_generate("<<Paste>>")

    # Segment menu functions
    def clear(self):
        self.sen_text_pad.delete(0, END)
        self.wrd_text_pad.delete('1.0', END)

    def segment_all(self):
        """
        If sentence segmentation has not yet been done,
        apply sentence segmentation and apply word segmentation to all sentences.
        If sentence segmentation has already been done,
        apply word segmentation to sentences selected.
        If no sentence is selected, regard as all sentences have been selected
        """
        if self.has_raw:
            self.clear()
            if not self.has_sen:
                self.sentence_segment()
            self.word_segment()
        else:
            messagebox.showerror("An error occurs", "There is no text to be segmented!")

    def sentence_segment(self):
        if self.has_raw:
            self.clear()
            aft_seg = self._sen_seg(self.raw_text_pad.get('1.0', 'end'))
            self.sen_text_pad.delete(0, END)
            for sen in aft_seg:
                self.sen_text_pad.insert('end', sen)
        else:
            messagebox.showwarning("An error occurs", "There is no text to be segmented!")

    def word_segment(self):
        """
        If sentence segmentation has already been done,
        apply word segmentation to sentences selected.
        If no sentence is selected, segment all sentences.
        """
        if self.has_sen:
            selected_sen = self.sen_text_pad.curselection()
            if not selected_sen:
                selected_sen = [i for i in range(self.sen_text_pad.size())]

            aft_seg = [self._wrd_seg(self.sen_text_pad.get(ind)) for ind in selected_sen]
            self.wrd_text_pad.delete('1.0', 'end')
            self.wrd_text_pad.insert('1.0', "\n".join(aft_seg))
        else:
            messagebox.showwarning("An error occurs", "There is no sentence to be segmented!")

    def file_to_file(self, first_in=True, src=None, des=None):
        """
        This function opens a file and directly export the result of word segmentation to another file
        Note:
        This function will call itself once with a minor delay to display 'Cutting' information
        in case users would think the app break down.
        All three paras work for this and by no means should caller give any para
        """
        src_file = src if src else filedialog.askopenfile()
        des_file = des if des else filedialog.asksaveasfile()

        if first_in:
            self.root.title("Cutting, wait a second...")
            self.root.after(200, lambda: self.file_to_file(False, src_file, des_file))
        else:
            des_file.write(self._wrd_seg(src_file.read()))
            self.root.title("Done")
            src_file.close()
            des_file.close()

    # Lexicon & Rules
    def load_rule_options(self, menu):
        """
        If rules haven't been initialized,it initialize rule variables first.
        Then add these rules to the menu,and return the menu
        """
        if not self.rule_booleans:
            self.rule_description = self._get_rules()
            for _ in self.rule_description:
                b = BooleanVar(value=True)
                self.rule_booleans.append(b)
                # FIXME: I want to memorize users' setting instead of set all to 1!

        for b, d in zip(self.rule_booleans, self.rule_description):
            menu.add_checkbutton(label=d, variable=b)

        return menu

    def show_lexicon_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(0)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(0)
            self.load_situ()
            self.load_term()

    def show_rule_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(1)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(1)
            self.load_situ()
            self.load_term()

    def load_lexicon(self):
        """Load lexicon and show in self.lex_pad"""
        lex = self._get_lex()
        for l in lex:
            self.lexi_pad.insert(END, l)

    def load_term(self):
        """Load term and show in self.term_pad"""
        lex = self._get_term()
        for l in lex:
            self.term_pad.insert(END, l)

    def load_situ(self):
        """Load term and show in self.situ_pad"""
        # FIXME: There are three almost same function load_lex/term/situ,combine them!
        lex = self._get_situ()
        for l in lex:
            self.situ_pad.insert(END, l)

    # Help & About
    def help(self):
        hlp = """Some instruction:
         1.Open a file into the first frame.
         2.Type in the first frame or edit it as you like.

         3.Click 'Sentence Segment' in the menu 'Segment' to segment the sentences.
         4.Select some sentences.
         5.Click 'Word Segment' in the menu 'Segment' to segment words.
         or
         3-5.Click 'Segment All' to segment everything.

         6.Click 'Export' in menu 'File' to export word segmentation result.
         7.See 'Data' menu to modify settings and data as you like.
         8.Enjoy it! :)
        """
        t = Toplevel(self.root)
        t.title("Help")
        t.transient(self.root)
        Label(t, text=hlp, justify=LEFT).pack(pady=5, padx=5)

    def about(self):
        abt = """This system is written as a assignment of SJTU IEEE."""

        cpyright = """Copyright (c) 2016 SJTU
    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose."""

        t = Toplevel(self.root)
        t.title("About")
        t.transient(self.root)
        Label(t, text=abt).pack(pady=8, padx=5)
        Label(t, text=cpyright, justify=LEFT).pack(pady=5, padx=5)

    @property
    def has_raw(self):
        """Whether any file has been loaded into text_pad"""
        return self.raw_text_pad.get('1.0', 'end').strip() != ""

    @property
    def has_sen(self):
        """Whether sentence segmentation has been made"""
        return self.sen_text_pad.get(0, 'end') != ()

    @property
    def has_wrd(self):
        """Whether word segmentation has been made"""
        return self.wrd_text_pad.get('1.0', 'end').strip() != ""

    # Extensions of scrollbar and listbox functions
    # ----------------------------------------------------------
    @staticmethod
    def add_scrollbar(obj):
        scrollbar = Scrollbar(obj.master)
        scrollbar.configure(command=obj.yview)
        obj.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=LEFT, fill=Y)

    def listbox_find(self, master: Listbox):
        """This function make a find window for a listbox"""
        find_window = Toplevel(self.root)
        find_window.title("Find")
        find_window.transient(master)

        Label(find_window, text="Find:")
        e = Entry(find_window)
        e.pack(padx=4, pady=4)

        def find():
            lex = master.get(0, END)
            target = e.get()
            try:
                ind = lex.index(target)
            except ValueError:
                messagebox.showerror(message="No such word!")
            else:
                master.select_clear(0, END)
                master.select_set(ind)
                master.see(ind)

        Button(find_window, text="Go!", command=find).pack(padx=4, pady=4)

    def listbox_add(self, master: Listbox):
        """This function make a add_item window for a listbox"""
        add_window = Toplevel(self.root)
        add_window.title("Add")
        add_window.transient(master)

        Label(add_window, text="Add:")
        target = StringVar()
        e = Entry(add_window, textvariable=target)
        e.pack(padx=4, pady=4)

        def add():
            item = e.get()
            if item in master.get(0, END):
                messagebox.showerror(message="This word already exists!")
            elif item.strip():
                master.insert(END, item)
                master.select_clear(0, END)
                master.select_set(END)
                master.see(END)

        Button(add_window, text="Add!", command=add).pack(padx=4, pady=4)

    def listbox_delete(self, master: Listbox):
        """This function delete a item for a listbox"""
        targets = master.curselection()
        if len(targets) == 1:
            master.delete(targets[0])
        elif len(targets) >= 2:
            messagebox.showerror(message="Too much items selected!\nDelete one item at once!")

    # Following functions involves conversation with controller
    # All interaction with controller are done below
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    def _sen_seg(self, raw: str) -> list:
        return self.controller.sentence_segment(raw)

    def _wrd_seg(self, raw: str) -> str:
        return self.controller.word_segment(raw)

    def _get_lex(self) -> list:
        return self.controller.get_lexicon()

    def _get_rules(self) -> list:
        return self.controller.get_rule_description()

    def _set_rules(self):
        self.controller.set_rule_booleans(self.rule_booleans)

    def _get_term(self) -> list:
        return self.controller.get_term()

    def _get_situ(self) -> list:
        return self.controller.get_particular_situation()