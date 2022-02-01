import re
from os.path import exists, dirname

# THESE PATHS WILL NOT WORK WHEN RUN FROM PYTHON INTERPRETER DUE TO THE RELIANCE ON __FILE__
PATH_TO_THIS_FILE = dirname(__file__)
DEFAULT_OUTPUT_FILE = PATH_TO_THIS_FILE + '\\..\\dictionary_files\\five_letter_words.txt'
DEFAULT_INPUT_FILE = PATH_TO_THIS_FILE + '\\..\\dictionary_files\\word_dictionary.txt'


def get_5_letter_word_file(file=DEFAULT_OUTPUT_FILE):
    create_5_letter_word_file_if_missing(file)
    return open(file, 'r')


def create_5_letter_word_file_if_missing(out_file_name=DEFAULT_OUTPUT_FILE, input_file=DEFAULT_INPUT_FILE):
    if not exists(out_file_name):
        create_5_letter_word_file(input_file, out_file_name)
    else:
        print("File \"{}\" exists. File will not be recreated.".format(out_file_name))


def create_5_letter_word_file(input_file_name, output_file_name):
    file, converted_file = open_files(input_file_name, output_file_name)

    five_letter_words = fetch_five_letter_words_from_file(file)

    alphabetic_non_acronym_lowercase_words = prepare_words_for_reading(five_letter_words)
    formatted_words_with_newlines_added = add_newlines_to_words(alphabetic_non_acronym_lowercase_words)

    converted_file.writelines(formatted_words_with_newlines_added)


def open_files(input_file, output_file):
    return open(input_file, 'r'), open(output_file, 'x')


def fetch_five_letter_words_from_file(file):
    word_lines_in_file = file.readlines()
    return get_5_letter_words_from_file_lines(word_lines_in_file)


def get_5_letter_words_from_file_lines(word_lines_in_file, wordle_word_length=5):
    return [word_line.strip() for word_line in word_lines_in_file if len(word_line.strip()) == wordle_word_length]


def prepare_words_for_reading(five_letter_words):
    alphabetic_words = [word for word in five_letter_words if word_is_alphabetic_only(word)]
    alphabetic_non_acronym_words = remove_acronyms_from_words(alphabetic_words)
    return make_all_words_lowercase(alphabetic_non_acronym_words)


def word_is_alphabetic_only(word):
    word_with_removed_chars = re.sub(r'[^A-za-z]+', '', word)

    if len(word_with_removed_chars) == len(word):
        return True
    return False


def remove_acronyms_from_words(words):
    return list(filter(lambda word: word != word.upper(), words))


def make_all_words_lowercase(words):
    return [word.lower() for word in words]


def add_newlines_to_words(words):
    return [(word + '\n') for word in words]


if __name__ == '__main__':
    create_5_letter_word_file_if_missing()
