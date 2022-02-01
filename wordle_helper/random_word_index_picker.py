from random import randint

from file_handler import get_5_letter_word_file
from main import get_5_letter_words_from_file

# TODO: make this a command line argument reader that lets you put in a guess and returns missed letters,
# correct letters, and incorrect letters based on the randomly generated value.

max_guesses = 6
num_guesses = 0
guesses = {}


def main():
    file = get_5_letter_word_file()
    words = get_5_letter_words_from_file(file)

    num_words = len(words)
    hidden_word_index = randint(0, num_words - 1)
    # print(index)

    print("Enter your guesses...")


if __name__ == '__main__':
    main()
