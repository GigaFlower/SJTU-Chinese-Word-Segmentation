"""Code responsible for GUI interface"""
from tkinter import *
from tkinter import messagebox


class DemoView:
    def __init__(self):
        # Root window
        self.root = Tk()
        self.root.title("Y")

        # Three main text pads
        self.raw_text_pad = Text()
        self.sen_text_pad = Text()
        self.wrd_text_pad = Text()

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
        segment_menu.add_command(label="File to file")

        # lexicon_menu
        lexicon_menu = Menu(main_menu)
        lexicon_menu.add_command(label="Load")
        lexicon_menu.add_command(label="Add")
        lexicon_menu.add_command(label="Modify")
        lexicon_menu.add_command(label="Delete")

        # rule_menu
        rule_menu = Menu(main_menu)
        rule_menu.add_command(label="Rule", command=self.rule_load())

        # help_menu
        help_menu = Menu(main_menu)
        help_menu.add_command(label="Help", command=self.help)
        help_menu.add_command(label="About", command=self.about)

        # main_menu
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Edit", menu=edit_menu)
        main_menu.add_cascade(label="Segment", menu=segment_menu)
        main_menu.add_cascade(label="Lexicon", menu=lexicon_menu)
        main_menu.add_cascade(label="Rule", menu=rule_menu)
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
    def sentence_segment(self):
        """
        If sentence segmentation has not yet been done,
        apply sentence segmentation and apply word segmentation to all sentences.
        If sentence segmentation has already been done
        apply word segmentation to sentences selected.
        If no sentence is selected, regard as all sentences have been selected
        """
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

    def file_to_file(self):
        pass

    # Lexicon & Rule
    def lexicon_load(self):
        pass
    def rule_load(self):
        pass

    # Help & About
    def help(self):
        pass
    def about(self):
        pass

    # Following functions involves conversation with controller
    # ----------------------------------------------------------
    def register(self, controller):
        """Make connection with controller"""
        self.controller = controller

    def _sen_seg(self, raw):
        return self.controller.sentence_segment(raw)

    def _wrd_seg(self, raw):
        return self.controller.word_segment(raw)


if __name__ == '__main__':
    t = DemoView()
    t.run()