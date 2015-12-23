"""Code responsible for GUI interface"""
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk


class DemoView:
    def __init__(self, controller):
        self.controller = controller
        # Root window
        self.root = Tk()
        self.root.title("Y")

        # Three main text pads
        # Only remind coder that there exist these properties
        # Actual initialization is done in self.make_XXX()
        self.raw_text_pad = Text()
        self.sen_text_pad = Text()
        self.wrd_text_pad = Text()

        self.setting_window = ttk.Notebook()
        self.setting_tabs = ttk.Notebook()
        self.lexi_pad = Text()
        self.rule_pad = Text()

        self.setting_window_on = False
        self.rule_booleans = {}

        self.set_text_pad()
        self.make_menu()

    def run(self):
        self.root.mainloop()

    def make_menu(self):
        main_menu = Menu(self.root)

        # file_menu
        file_menu = Menu(main_menu)
        file_menu.add_command(label="New", accelerator="Ctrl+N")
        file_menu.add_command(label="Open", accelerator="Ctrl+O")
        file_menu.add_command(label="Open Recent")
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S")
        file_menu.add_command(label="Save As")
        file_menu.add_separator()
        file_menu.add_command(label="Export")
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q")

        # edit_menu
        edit_menu = Menu(main_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", accelerator="Shift+Ctrl+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        edit_menu.add_command(label="Find_All", accelerator="Ctrl+F", command=self.find_all)

        # segment_menu
        segment_menu = Menu(main_menu)
        segment_menu.add_command(label="Sentence Segment", command=self.sentence_segment)
        segment_menu.add_command(label="Word Segment", command=self.word_segment)
        segment_menu.add_command(label="Segment all", command=self.segment_all)
        segment_menu.add_command(label="File to file", command=self.file_to_file)

        # data_menu
        data_menu = Menu(main_menu)
        data_menu.add_command(label="Lexicon", command=self.show_lexicon_pane)
        data_menu.add_command(label="Rule", command=self.show_rule_pane)

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

    def set_text_pad(self):
        """This function setting the properties of raw_text_pad,sen_text_pad and wrd_text_pad"""
        # setting raw_text_pad
        self.raw_text_pad = Text(self.root)
        self.raw_text_pad.pack()

        # setting sen_text_pad
        self.sen_text_pad = Text(self.root)
        self.sen_text_pad.pack()

        # setting wrd_text_pad
        self.wrd_text_pad = Text(self.root)
        self.wrd_text_pad.pack()

    def make_setting_pad(self, tab=0):
        """Make setting_pad which is to be trigger from clicking at 'Lexicon' or 'Rule' in menu"""
        self.setting_window = Toplevel()
        self.setting_window.minsize(400, 200)
        self.setting_window.resizable = False

        # Override window delete function
        def delete_setting_window():
            self.setting_window_on = False
            self.setting_window.destroy()
        self.setting_window.protocol('WM_DELETE_WINDOW', delete_setting_window)

        # Make notebook
        self.setting_tabs = ttk.Notebook(self.setting_window)

        # Make lexicon_tab
        lexicon_tab = Frame(self.setting_tabs)
        self.lexi_pad = Listbox(lexicon_tab)
        self.lexi_pad.pack(side=LEFT)

        Button(lexicon_tab, text='Load', width=7, command=self.load_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Add', width=7, command=self.add_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Search', width=7, command=self.search_lexicon).pack(expand=True)

        Button(lexicon_tab, text='Delete', width=7, command=self.delete_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Modify', width=7, command=self.modify_lexicon).pack(expand=True, padx=5)

        # Make rule_tab
        rule_tab = Frame(self.setting_tabs)
        self.rule_pad = Frame(rule_tab)
        self.load_rule()
        self.rule_pad.pack()

        #
        self.setting_tabs.add(lexicon_tab, text="Lexicon")
        self.setting_tabs.add(rule_tab, text="Rule")
        self.setting_tabs.select(tab)
        self.setting_tabs.pack(expand=True, fill=BOTH)

    # Menu functions
    # ----------------------------------------------------------
    # File menu
    def new(self):
        pass
    def open(self):
        pass
    def save(self):
        pass
    def save_as(self):
        pass
    def exit(self):
        pass

    # Edit menu
    def undo(self):
        pass
    def redo(self):
        pass
    def cut(self):
        pass
    def copy(self):
        pass
    def paste(self):
        pass
    def find_all(self):
        pass

    # Segment menu
    def segment_all(self):
        """
        If sentence segmentation has not yet been done,
        apply sentence segmentation and apply word segmentation to all sentences.
        If sentence segmentation has already been done,
        apply word segmentation to sentences selected.
        If no sentence is selected, regard as all sentences have been selected
        """
        if not self.has_raw:
            messagebox.showerror("An error occurs", "There is no text to be segmented!")
        elif not self.has_sen:
            self.sentence_segment()
            # FIXME: Should be all sentences but this function is unavailable yet
        else:
            self.sentence_segment()

    def sentence_segment(self):
        raw = self.raw_text_pad.get('1.0', 'end')
        raw = raw.strip()
        if raw:
            aft_seg = self._sen_seg(raw)
            self.sen_text_pad.delete('1.0', 'end')
            self.sen_text_pad.insert('1.0', aft_seg)
        else:
            messagebox.showwarning("An error occurs", "There is no text to be segmented!")

    def word_segment(self):
        raw = self.sen_text_pad.get('1.0', 'end')
        raw = raw.strip()
        if raw:
            aft_seg = self._wrd_seg(raw)
            self.wrd_text_pad.delete('1.0', 'end')
            self.wrd_text_pad.insert('1.0', aft_seg)
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

    # Lexicon & Rule
    def show_lexicon_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(0)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(tab=0)

    def show_rule_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(1)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(tab=1)

    def load_lexicon(self):
        """Load lexicon and show in self.lex_pad"""
        lex = self._get_lexicon()
        for l in lex:
            self.lexi_pad.insert(END, l)

    def add_lexicon(self):
        pass
    def search_lexicon(self):
        pass
    def delete_lexicon(self):
        pass
    def modify_lexicon(self):
        pass

    def load_rule(self):
        """Load rules and add corresponding checkbutton to self.rule_pad"""
        self.rule_booleans = {}
        rul = self._get_rules()
        for r in rul:
            b = BooleanVar()
            self.rule_booleans[r] = b
            Checkbutton(self.rule_pad, text=r, variable=b).pack(expand=True, fill=BOTH)
            # FIXME: I want to memorize users' setting instead of set all to 0!

    # Help & About
    def help(self):
        pass
    def about(self):
        pass

    @property
    def has_raw(self):
        """This function is used to check whether any file has been loaded"""
        return self.raw_text_pad.get('1.0', 'end').strip() != ""

    @property
    def has_sen(self):
        """This function is used to check whether sentence segmentation has been made"""
        return self.sen_text_pad.get('1.0', 'end').strip() != ""

    # Following functions involves conversation with controller
    # All interaction with controller are done below
    # ----------------------------------------------------------
    def _sen_seg(self, raw: str) -> str:
        return self.controller.sentence_segment(raw)

    def _wrd_seg(self, raw: str) -> str:
        return self.controller.word_segment(raw)

    def _get_lexicon(self) -> list:
        return self.controller.get_lexicon()

    def _get_rules(self) -> list:
        return self.controller.get_rule_description()
