"""Code responsible for application logic"""

import view
import kernel


class MainController:
    """The main controller of app activity"""
    def __init__(self):
        self.kernel = kernel.Segmentation()
        self.view = view.View(self)

    def run(self):
        self.view.run()

    def sentence_segment(self, raw: str) -> list:
        """
        This function receive complete long string from View,
        ask for Model to do sentence segmentation,
        return processed string list to View.

        Examples:
        >>> c = MainController()
        >>> c.sentence_segment("你好，再见。")
        ['你好，', '再见。']

        """
        aft_seg = self.kernel.sentence_segment(raw)
        aft_seg = [x for x in aft_seg if x.strip()]
        return aft_seg

    def word_segment(self, sentence: str) -> str:
        """
        This function receive a sentence from View,
        ask Model to do word segmentation,
        return processed string to View.

        Examples:
        >>> c = MainController()
        >>> c.word_segment("我喜欢足球")
        '我|喜欢|足球'
        """
        return self.kernel.word_segment(sentence)

    def get_lexicon(self) -> list:
        """
        Get lexicon from self.kernel
        like {'姑娘':25686900,...}
        (it should be a really big dictionary)
        """
        lex = self.kernel.get_word_lexicon()
        return sorted(lex.keys())

    def get_term(self) -> list:
        """
        Get terms from self.kernel
        like {'中华人民共和国':['TERM'],...}
        """
        lex = self.kernel.get_term_lexicon()
        return sorted(lex.keys())

    def get_particular_situation(self) -> list:
        """
        Get particular situation description from self.kernel
        like {'先后来到':['bound','separated','bound']}
        denoting how this particular word should be segmented
        After format into '先后来到\t->\t先后|来到',
        return to view.
        """
        sit = self.kernel.get_situ()
        ret = []
        for k, v in sorted(sit.items()):
            assert(len(k) == len(v)+1)
            raw = k
            after_format = k[0]
            for ind in range(len(v)):
                if v[ind] == 'separated':
                    after_format += '|'
                after_format += k[ind+1]
            ret.append("%s\t->\t%s" % (raw, after_format))

        return ret

    def get_rule_description(self) -> list:
        """Get rules from self.kernel"""
        return self.kernel.get_rule_description()

    def set_rule_booleans(self, bools):
        """Tell self.kernel which rule need to be obeyed"""
        self.kernel.set_rule_boolean(bools)

    def modify(self, data: str, operation: str, data_type: str):
        assert(data_type in ("lexi", "term", "situ"))
        assert(operation in ("add", "delete"))

        if data_type == "lexi":
            if operation == 'add':
                self.kernel.lexicon_add_word([data, "5", "N"])  # Here "5" and "N" are arbitrary
            elif operation == 'delete':
                self.kernel.lexicon_delete_word(data)

        elif data_type == "term":
            if operation == 'add':
                self.kernel.lexicon_add_word([data, "5", "TERM"])
            elif operation == 'delete':
                self.kernel.lexicon_delete_word(data)

        elif data_type == "situ":
            # data should be like "ABCDE -> A|BC|DE"
            # We need decompose it first
            tmp = data.split("->")
            data = tmp[0].strip()
            tmp[1] = tmp[1].strip()

            ind = [tmp[1].index(ch) for ch in data]  # [0,2,3,5,6]
            d_ind = [ind[i]-i for i in range(len(ind))]  # [0,1,1,2,2]

            string = ""
            for i in range(len(d_ind)-1):
                if d_ind[i+1] != d_ind[i]:
                    string += 'separated,'
                else:
                    string += 'bound,'
            string = string[:-1]

            if operation == 'add':
                self.kernel.lexicon_particular_situation([data, string])
            elif operation == 'delete':
                self.kernel.lexicon_delete_particular_situation(data)

    def rebuild(self):
        self.kernel.lexicon_reinitialization()

if __name__ == '__main__':
    import doctest
    doctest.testmod()