import re
import string

import command_line_reader
import file_handler


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


def get_top_five_most_common_characters(all_words_list):
    dictionary = dict.fromkeys(string.ascii_lowercase, 0)
    for word in all_words_list:
        for character in word.strip():
            if (not character == '_') and (character not in dictionary):
                raise Exception("Non-alphabetic character: " + character)
            else:
                dictionary[character] = dictionary[character] + 1  # increment count for character
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


def find_words_with_characters_at_indexes(words, index_list):
    return list(filter(
        lambda word:
        ((index_list[0] is None) or word[0] == index_list[0])
        and ((index_list[1] is None) or word[1] == index_list[1])
        and ((index_list[2] is None) or word[2] == index_list[2])
        and ((index_list[3] is None) or word[3] == index_list[3])
        and ((index_list[4] is None) or word[4] == index_list[4])
        , words))


def find_words_with_characters(words, character_list):
    return [word for word in words if all(character in word for character in character_list)]


def find_words_with_characters_for_guesses_out_of_place(words, guesses):
    good_words = []
    for word in words:
        for guess in guesses:
            word_if_good = filter_words_by_correct_characters_in_wrong_places(word, guess)
            if word_if_good is not None:
                good_words.append(word_if_good.strip())
    return good_words


def filter_words_by_correct_characters_in_wrong_places(word, guess):
    for i in range(len(guess)):
        current_char = guess[i]
        if (not current_char == '_') and (current_char in word and (not word.index(guess[i]) == i)):
            return None
    return word


def remove_words_from_list_with_characters(word_list, character_list):
    words = [word for word in word_list if all(char not in word for char in character_list)]
    return words


def get_sorted_available_non_zero_counts(available_words):
    available_counts = get_top_five_most_common_characters(available_words)
    available_counts = dict(filter(lambda element: element[1] > 0, available_counts.items()))
    return dict(sorted(available_counts.items(), key=lambda item: item[1], reverse=True))


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


def filter_words_to_possible_words(words, incorrect_chars, correct_chars, chars_out_of_place):
    found_words = find_words_with_characters_for_guesses_out_of_place(words, chars_out_of_place)
    found_words = find_words_with_characters_at_indexes(found_words, correct_chars)
    available_words = remove_words_from_list_with_characters(found_words, incorrect_chars)
    return available_words


def filter_char_counts_base_off_of_remaining_words(available_words):
    return get_sorted_available_non_zero_counts(available_words)


def character_count_stats(file, incorrect_chars=None, correct_chars=None, chars_out_of_place=None, print_ranked=False,
                          print_stats=False):
    if chars_out_of_place is None:
        chars_out_of_place = []
    if incorrect_chars is None:
        incorrect_chars = []
    if correct_chars is None:
        correct_chars = []

    five_letter_words = [word.strip() for word in file.readlines()]  # Remove newline characters from the words

    if print_ranked:
        character_position_counts = create_count_dictionaries_for_letter_placements(five_letter_words)
        print_ranked_chars(character_position_counts)

    if print_stats:
        total_character_counts_dict = get_top_five_most_common_characters(five_letter_words)
        print("total character counts: ",
              dict(sorted(total_character_counts_dict.items(), key=lambda item: item[1], reverse=True)))

    available_words = filter_words_to_possible_words(five_letter_words, incorrect_chars, correct_chars,
                                                     chars_out_of_place)
    available_counts = filter_char_counts_base_off_of_remaining_words(available_words)

    if print_stats:
        print("available words: ", available_words)

    print("available counts: ", available_counts)


def main():
    file = file_handler.get_5_letter_word_file()
    args = command_line_reader.read_command_line_args()

    incorrect_chars, misplaced_chars, correct_chars, print_ranked, print_all = args
    character_count_stats(file, incorrect_chars, correct_chars, misplaced_chars, print_ranked, print_all)


if __name__ == '__main__':
    main()
