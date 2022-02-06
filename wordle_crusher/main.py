import re
import string

from wordle_crusher import file_handler, command_line_reader, word_filter, word_optimizer


def word_is_alphabetic_only(word):
    word_with_removed_chars = re.sub(r'[^A-za-z]+', '', word)

    if len(word_with_removed_chars) == len(word):
        return True
    return False


def create_count_dictionaries_for_letter_placements(all_words_list):
    """Returns a tuple of dictionaries where the index of the tuple is the counts for that index of each word

    >>> create_count_dictionaries_for_letter_placements(all_words_list)
    (dictPosition0, dictPosition1, dictPosition2, dictPosition3, dictPosition4)

    For example:
    dictPosition0 has the counts of all characters (a-z) in the first position of all the words.
    dictPosition3 has the counts of all characters (a-z) in the fourth position of all the words.
    """
    dictPosition0 = create_dictionary_of_characters_at_word_index(0, all_words_list)
    dictPosition1 = create_dictionary_of_characters_at_word_index(1, all_words_list)
    dictPosition2 = create_dictionary_of_characters_at_word_index(2, all_words_list)
    dictPosition3 = create_dictionary_of_characters_at_word_index(3, all_words_list)
    dictPosition4 = create_dictionary_of_characters_at_word_index(4, all_words_list)

    return dictPosition0, dictPosition1, dictPosition2, dictPosition3, dictPosition4


def create_dictionary_of_characters_at_word_index(index, all_words_list):
    dictionary = dict.fromkeys(string.ascii_lowercase, 0)
    for word in all_words_list:
        if word[index] not in dictionary:
            raise Exception("Non-alphabetic character: " + str(word[index]))
        else:
            dictionary[word[index]] = dictionary[word[index]] + 1  # increment count for character at index
    return dictionary


def get_n_most_max_character_counts_tuple(dictionary, n):
    """Returns a tuple containing the character with the n'th highest count in the dictionary along with its count
    >>> get_n_most_max_character_counts_tuple(dictionary, 5)
    ('x', 1234)

    >>> get_n_most_max_character_counts_tuple(dictionary, 6)
    ('y', 1233)

    >>> get_n_most_max_character_counts_tuple(dictionary, 7)
    ('z', 1232)
    """
    dictn = dictionary.copy()
    for i in range(n - 1):
        max_char = max(dictn, key=dictn.get)
        del dictn[max_char]

    n_max = max(dictn, key=dictn.get)
    return n_max, dictn[n_max]


def find_words_with_characters(words, character_list):
    return [word for word in words if all(character in word for character in character_list)]


def ordinal(num):
    """
    Magic that appends the order to the n'th number example: 'th is the ordinal of 4, which gives us 4'th.
    >>> ordinal(1)
    1'st
    >>> ordinal(3)
    3'rd
    >>> ordinal(4)
    4'th
    >>> ordinal(21)
    21'st
    """
    return "%d%s%s" % (num, "'", "tsnrhtdd"[(num // 10 % 10 != 1) * (num % 10 < 4) * num % 10::4])


def print_ranked_chars(character_position_counts):
    for n in range(1, 27):
        n_max_counts = [get_n_most_max_character_counts_tuple(count_dictionary, n) for count_dictionary in
                        character_position_counts]
        print(ordinal(n), " most common characters at positions: ", n_max_counts, sep='')


def is_no_char_inputs(incorrect_inputs, out_of_place_inputs, correct_inputs):
    no_incorrect_chars = len(incorrect_inputs) == 0
    no_chars_out_of_place = len(out_of_place_inputs) == 0
    no_correct_chars = all(char is None for char in correct_inputs)
    return no_incorrect_chars and no_chars_out_of_place and no_correct_chars


def character_count_stats(five_letter_words, incorrect_chars=None, correct_chars=None, chars_out_of_place=None,
                          print_ranked=False):
    if chars_out_of_place is None:
        chars_out_of_place = []
    if incorrect_chars is None:
        incorrect_chars = []
    if correct_chars is None:
        correct_chars = []

    available_words = word_filter.filter_words_to_possible_words(five_letter_words.copy(),
                                                                 incorrect_chars.copy(),
                                                                 correct_chars.copy(),
                                                                 chars_out_of_place.copy())

    total_character_counts = word_filter.get_total_char_counts_sorted_based_off_of_remaining_words(
        available_words.copy())
    character_counts_by_word = word_filter.get_sorted_char_counts_based_off_of_remaining_words(available_words.copy())

    if print_ranked:
        character_position_counts = create_count_dictionaries_for_letter_placements(five_letter_words.copy())
        print_ranked_chars(character_position_counts)

    total_character_counts_dict = word_filter.create_character_in_word_count_dict(five_letter_words.copy())
    print("total character counts for all words in dictionary: ",
          dict(sorted(total_character_counts_dict.items(), key=lambda item: item[1], reverse=True)))

    sorted_words = word_optimizer.order_and_print_words_by_most_likely_from_available_words_and_character_counts(
        character_counts_by_word.copy(),
        total_character_counts.copy(),
        available_words.copy())

    print("Sorted available words by likeliness: ", sorted_words)
    print("Counts of chars in words:", character_counts_by_word)


def get_5_letter_words_from_file(file):
    return [word.strip() for word in file.readlines()]


def main():
    file = file_handler.get_5_letter_word_file()
    args = command_line_reader.read_command_line_args()

    incorrect_chars, misplaced_chars, correct_chars, print_ranked, total = args
    five_letter_words = get_5_letter_words_from_file(file)

    if total:
        print("Total number of words in the dictionary: ", len(five_letter_words))

    character_count_stats(five_letter_words, incorrect_chars, correct_chars, misplaced_chars, print_ranked)


if __name__ == '__main__':
    main()
