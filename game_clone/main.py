import shlex
from random import randint

from wordle_crusher.file_handler import get_5_letter_word_file
from wordle_crusher.main import get_5_letter_words_from_file

# Emojis
# MISS = '\U0001F937'
# CORRECT = '\U0001F389'
# INCORRECT = '\U0001F4A9'

# Letters
MISS = 'M'
CORRECT = 'C'
INCORRECT = 'I'

guesses = []  # A list of tuples (character, index, hit/miss/incorrect)
MAX_GUESSES = 6  # if word is not in dictionary it doesn't count toward guesses.
num_guesses = 0


def main():
    file = get_5_letter_word_file()
    words = get_5_letter_words_from_file(file)

    num_words = len(words)
    hidden_word_index = randint(0, num_words - 1)
    hidden_word = words[hidden_word_index]
    # print(hidden_word_index)

    print("Enter your guesses...")
    print('To get help, enter `help`.')

    while True:
        cmd, *args = shlex.split(input(
            '> '))  # TODO how to gracefully handle hitting enter with nothing entered. How to handle more than one word
        if cmd == 'exit' or cmd == 'q' or cmd == 'quit':
            break
        else:
            result = process_command_and_args(cmd, args, words, hidden_word)
            if result:
                break


def process_command_and_args(cmd, args, words, hidden_word):
    if cmd == 'help':
        print("I still need to implement this, sorry...")
        return False
    else:
        return check_guess_against_word_and_print_results(cmd, words, hidden_word)


def check_guess_against_word_and_print_results(guess, words, hidden_word):
    if not validate_guess(guess, words):
        return False

    print("You guessed: ", guess)
    result = check_guess_against_word(guess, hidden_word)
    guesses.append(result)
    print("Result of guesses:")
    print_guess_results(guesses)

    global MAX_GUESSES
    global num_guesses
    num_guesses = num_guesses + 1

    if guess == hidden_word:
        print("Congrats, you won!")
    elif num_guesses == MAX_GUESSES:
        print("You have run out of guesses... the correct word was:", hidden_word)
        return True
    else:
        print("Try again.")
    return False


def print_guess_results(guesses):
    for guess in guesses:
        print(guess)


def validate_guess(guess, words):
    if not guess.isalpha():
        print("Your guess, {},contains non-alphabetic characters. Please try with only alphabetic characters.".format(
            guess))
        return False
    elif len(guess) != 5:
        print("Your guess, {}, needs to be exactly 5 characters long. Your guess was {} characters long.".format(guess,
                                                                                                                 len(guess)))
        return False
    elif guess not in words:
        print("Your guess, {}, does not exist in the dictionary. Try again.".format(guess))
        return False
    else:
        return True


def check_guess_against_word(guess, hidden_word):
    split_word = list(hidden_word)
    split_guess = list(guess)

    guess_result = []

    for i in range(len(split_word)):
        character = split_guess[i]
        accuracy = get_accuracy_of_character_in_word(character, split_word, i)
        guess_result.append((character, accuracy))

    return guess_result


def get_accuracy_of_character_in_word(character, split_word, index):
    if character in split_word:
        if character == split_word[index]:
            return CORRECT
        else:
            return MISS
    else:
        return INCORRECT


if __name__ == '__main__':
    main()
