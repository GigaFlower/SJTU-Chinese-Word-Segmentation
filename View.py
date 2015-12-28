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
        self.sen_text_pad = Listbox()
        self.wrd_text_pad = Text()

        self.setting_window = ttk.Notebook()
        self.setting_window_on = False
        self.setting_tabs = ttk.Notebook()

        self.lexi_pad = Listbox()
        # No self.rule_pad because rules don't need lazy load.

        self.rule_booleans = []
        self.rule_description = []

        self.make_text_pad()
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
        segment_menu.add_command(label="Clear", accelerator="Shift+Ctrl+C", command=self.clear)

        # data_menu
        data_menu = Menu(main_menu)
        data_menu.add_command(label="Lexicon", command=self.show_lexicon_pane)
        rule_menu = Menu(data_menu)
        rule_menu = self.load_rules(rule_menu)
        rule_menu.add_separator()
        rule_menu.add_command(label="Edit", command=self.show_rule_pane)
        data_menu.add_cascade(label="Rules", menu=rule_menu)

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
        self.setting_window.resizable = False

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
        self.lexi_pad = Listbox(lexicon_tab)
        scrollbar = Scrollbar(lexicon_tab)
        scrollbar.configure(command=self.lexi_pad.yview)
        self.lexi_pad.configure(yscrollcommand=scrollbar.set)
        self.lexi_pad.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=LEFT, fill=Y)

        Button(lexicon_tab, text='Load', width=7, command=self.load_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Add', width=7, command=self.add_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Search', width=7, command=self.search_lexicon).pack(expand=True)

        Button(lexicon_tab, text='Delete', width=7, command=self.delete_lexicon).pack(expand=True)
        Button(lexicon_tab, text='Modify', width=7, command=self.modify_lexicon).pack(expand=True, padx=5)

        # Make rule_tab
        rule_tab = Frame(self.setting_tabs)
        Label(rule_tab, text="Particular situation:").grid(row=0, column=0)
        Label(rule_tab, text="Proper nouns:").grid(row=0, column=1)
        rule_pad_A = Listbox(rule_tab)
        rule_pad_A.grid(row=1, column=0)
        rule_pad_B = Listbox(rule_tab)
        rule_pad_B.grid(row=1, column=1)

        #
        self.setting_tabs.add(lexicon_tab, text="Lexicon")
        self.setting_tabs.add(rule_tab, text="Rules")
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
    def show_lexicon_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(0)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(0)

    def show_rule_pane(self):
        if self.setting_window_on:
            self.setting_tabs.select(1)
            self.setting_window.focus_set()
        else:
            self.setting_window_on = True
            self.make_setting_pad(1)

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

    def load_rules(self, menu):
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

    # Help & About
    def help(self):
        pass
    def about(self):
        pass

    @property
    def has_raw(self):
        """Whether any file has been loaded into text_pad"""
        return self.raw_text_pad.get('1.0', 'end').strip() != ""

    @property
    def has_sen(self):
        """Whether sentence segmentation has been made"""
        return self.sen_text_pad.get(0, 'end') != ()

    # Following functions involves conversation with controller
    # All interaction with controller are done below
    # ----------------------------------------------------------
    def _sen_seg(self, raw: str) -> list:
        return self.controller.sentence_segment(raw)

    def _wrd_seg(self, raw: str) -> str:
        return self.controller.word_segment(raw)

    def _get_lexicon(self) -> list:
        return self.controller.get_lexicon()

    def _get_rules(self) -> list:
        return self.controller.get_rule_description()

    def _set_rules(self):
        self.controller.set_rule_booleans(self.rule_booleans)

