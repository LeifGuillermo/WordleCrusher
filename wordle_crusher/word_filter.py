import string


def filter_words_to_possible_words(words, incorrect_chars, correct_chars, chars_out_of_place):
    """
    Filters the available words.
    First it finds available words with the provided 'chars_out_of_place' characters such that those characters
    do not appear in the same location as described by chars_out_of_place..
    Then, it removes words that have characters at their correct indexes described by correct_chars.
    Finally, it removes words with any of the incorrect_chars in them.
    """
    words = filter_words_containing_characters(words.copy(), chars_out_of_place.copy())
    words = find_words_with_characters_at_indexes(words.copy(), correct_chars)
    words = remove_words_from_list_with_characters(words.copy(), incorrect_chars)
    words = filter_words_by_characters_out_of_place(words.copy(), chars_out_of_place.copy())

    return sorted(words)


def filter_words_containing_characters(words, guesses):
    guesses_copy = guesses.copy()
    guess_chars = get_chars_from_guesses(guesses_copy)

    return [word for word in words if word_contains_all_characters_in_character_list(word, guess_chars)]


def word_contains_all_characters_in_character_list(word, character_list):
    return 0 not in [char in word for char in character_list]


def filter_words_by_characters_out_of_place(words, guesses):
    """
    :param words: list of all words remaining in the dictionary
    :param guesses: a list of guess-strings consisting of underscores and characters.
    :return: a set of good words that have been filtered using the guesses
    """
    if guesses is None or len(guesses) == 0:
        return words

    char_indices = create_guess_char_indices_dict(guesses)
    good_words = filter_words_with_characters_not_in_positions(words, char_indices)

    return good_words


def get_chars_from_guesses(guesses):
    """
    gets characters from guesses (removes underscores), removes duplicates and sorts them in an array which is returned.
    example guess: "__cr_"
    """
    guesses_copy = guesses.copy()
    guesses_copy = "".join(guesses_copy)
    return sorted("".join(set(guesses_copy.replace("_", ""))))  # remove duplicates and remove underscores.


def filter_words_with_characters_not_in_positions(words, char_indices):
    """
    Loops through char_indices which is a dictionary of character keys to indices where that character is not allowed
    (values) to show up in each word. If the char shows up in a word at the specified indices then the word is not
    included in the final list that this method produces.
    :return a set of good words
    """
    word_goodness = {}
    for word in words:
        for char in list(char_indices.keys()):
            word_is_good = not word_contains_char_at_indices(word, char, char_indices[char])
            if not word_is_good:
                word_goodness[word] = False
            elif word_is_good and not ((word in list(word_goodness.keys())) and (not word_goodness[word])):
                word_goodness[word] = True
    good_words = [word for word in word_goodness.keys() if word_goodness[word] is True]
    return set(good_words)


def word_contains_char_at_indices(word, char, indices):
    indices_of_char_in_word = find_all_indices_of_char_in_word(word, char)
    char_guesses_have_indices_in_word = any(item in indices for item in indices_of_char_in_word)
    char_is_in_word = char_guesses_have_indices_in_word
    return char_is_in_word


def find_all_indices_of_char_in_word(word, character):
    return [index for index, letter in enumerate(word) if letter == character]


def create_guess_char_indices_dict(guesses):
    """
    Loops over each guess, and then loops over each character in the guess. This method finds the index of the character
    in the guess and then appends it to a list of indices which are set as the value of the character (key) in the
    result map. Each non-underscore character in the guess is a key, and each key has a list of indices as its value.
    :param guesses: a string representing a guess. e.g. __c__ represents a guess with c in the 2nd index position.
    :return: a dictionary containing chars as keys and a list of indices from the guess as the value of each key
    """
    char_indices = dict()
    for guess in guesses:
        for i in range(len(guess)):
            char = guess[i]
            if not char == '_':
                if char in char_indices.keys():
                    char_indices[char].append(i)
                else:
                    char_indices[char] = [i]
    return char_indices


def get_character_indices(char, index):
    indices = []
    if not char == '_':
        indices.append(index)
    return indices


def find_words_with_characters_at_indexes(words, index_list):
    return list(filter(
        lambda word:
        ((index_list[0] is None) or word[0] == index_list[0])
        and ((index_list[1] is None) or word[1] == index_list[1])
        and ((index_list[2] is None) or word[2] == index_list[2])
        and ((index_list[3] is None) or word[3] == index_list[3])
        and ((index_list[4] is None) or word[4] == index_list[4])
        , words))


def remove_words_from_list_with_characters(word_list, character_list):
    words = [word for word in word_list if all(char not in word for char in character_list)]
    return words


def get_sorted_char_counts_based_off_of_remaining_words(available_words):
    available_counts = create_character_in_word_count_dict(available_words)
    return remove_zero_counts_from_characters_and_sort_into_dictionary(available_counts)


def get_total_char_counts_sorted_based_off_of_remaining_words(available_words):
    available_counts = create_total_character_count_dict(available_words)
    return remove_zero_counts_from_characters_and_sort_into_dictionary(available_counts)


def remove_zero_counts_from_characters_and_sort_into_dictionary(available_counts):
    available_counts = dict(filter(lambda element: element[1] > 0, available_counts.items()))
    return dict(sorted(available_counts.items(), key=lambda item: item[1], reverse=True))


def create_total_character_count_dict(all_words_list):
    dictionary = dict.fromkeys(string.ascii_lowercase, 0)
    for word in all_words_list:
        for character in word.strip():
            if character not in dictionary:
                raise Exception("Non-alphabetic character: " + character)
            else:
                dictionary[character] = dictionary[character] + 1  # increment count for character
    return dictionary


def create_character_in_word_count_dict(all_words_list):
    dictionary = dict.fromkeys(string.ascii_lowercase, 0)
    for word in all_words_list:
        for character in set(word.strip()):
            if character not in dictionary:
                raise Exception("Non-alphabetic character: " + character)
            else:
                dictionary[character] = dictionary[character] + 1  # increment count for character
    return dictionary
