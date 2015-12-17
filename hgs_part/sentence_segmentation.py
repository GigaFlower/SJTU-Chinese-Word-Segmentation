def read_origin_file():
    f = open("original_file.txt", "r", encoding="utf-16")
    ret = f.read()
    f.close()
    return ret


def read_punctuation_standard_file():
    f = open("punctuation_standard_file.txt", "r", encoding="utf-16")
    ret = f.read()
    f.close()
    return ret


def cut(string, punc_stan):
    """
    We will cut the whole string into several sentences according to the sentence segment punctuations.
    The punctuations are reserved, but there exists a special case that "\n" should be deleted.
    The completed sentences will be put in the list "s_complete".
    """
    substring = ""
    string_complete = []
    for cha in string:
        if cha == "\n":
            string_complete.append(substring)  # The linebreak "\n" is not included.
            substring = ""
        else:
            substring += cha
            if cha in punc_stan:
                string_complete.append(substring)
                # If the sentence segment punctuations("\n" is excluded) are detected,
                #  the sentence should be cut here.
                substring = ""
            else:
                pass
    return string_complete


# Main 
def main():
    whole_string = read_origin_file()
    punc_standard = read_punctuation_standard_file()  # "punc_standard" are sentence segment punctuations.

    string_cut = cut(whole_string, punc_standard)

    return string_cut

if __name__ == '__main__':
    main()
