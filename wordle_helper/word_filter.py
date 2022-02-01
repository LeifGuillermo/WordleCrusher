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
    Loops through char_indices which is a dictionary of characters to indices where that character is not allowed
    to show up in each word. If the char shows up in a word at the specified indices then the word is not included
    in the final list that this method produces.
    """
    word_goodness = {}
    for word in words:
        for char in list(char_indices.keys()):
            word_is_good = not word_contains_char_at_indices(word, char, char_indices[char])
            if not word_is_good:
                word_goodness[word] = False
            if word_is_good and not ((word in word_goodness.keys()) and (not word_goodness[word] is False)):
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
    char_indices = dict()
    for guess in guesses:
        for i in range(len(guess)):
            char = guess[i]
            if not char == '_':
                if char in char_indices.keys():
                    char_indices[char].append(i)
                else:
                    char_indices[char] = [i]
                add_non_underscore_char_index_to_guess_list(char, i, char_indices)
    return char_indices


def get_character_indices(char, index):
    indices = []
    if not char == '_':
        indices.append(index)
    return indices


def add_non_underscore_char_index_to_guess_list(char, index, char_indices):
    pass


# if not char == '_':
# if char not in char_indices.keys():
#     char_indices[char] = [index]
# else:
#     char_indices[char] = char_indices[char].copy().append(index)


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


# ##################

def filter_char_counts_base_off_of_remaining_words(available_words):
    return get_sorted_available_non_zero_counts(available_words)


def get_sorted_available_non_zero_counts(available_words):
    available_counts = get_top_five_most_common_characters(available_words)
    available_counts = dict(filter(lambda element: element[1] > 0, available_counts.items()))
    return dict(sorted(available_counts.items(), key=lambda item: item[1], reverse=True))


def get_top_five_most_common_characters(all_words_list):
    dictionary = dict.fromkeys(string.ascii_lowercase, 0)
    for word in all_words_list:
        for character in word.strip():
            if character not in dictionary:
                raise Exception("Non-alphabetic character: " + character)
            else:
                dictionary[character] = dictionary[character] + 1  # increment count for character
    return dictionary
