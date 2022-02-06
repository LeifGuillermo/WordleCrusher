def order_and_print_words_by_most_likely_from_available_words_and_character_counts(word_character_counts,
                                                                                   total_character_counts,
                                                                                   available_words):
    """
    Creates a list ordered by likeliness to be the hidden word or lead us closer to the hidden word.
    Two sorts are done. First a sort based off of characters existing in words. Second, just to break ties, a second
    sort is applied based off of total character counts.
    A word is most likely, in this sense, to be correct if it contains more higher-count characters.
    each character in each word is only counted once (by turning the characters of the word into a set)
    This method assumes available words is alphabetically sorted and character counts are sorted by value-descending.

    :param total_character_counts: a dictionary of character keys to count values.
    :param available_words: a list of available words
    :param word_character_counts: a dictionary of character keys to count values.
    :return: a sorted list of words ordered by their likelihood to be right (based off of character counts and which
    characters are in the word).
    """

    # word_char_ranks = get_char_ranks(word_character_counts)
    # total_char_ranks = get_char_ranks(total_character_counts)
    # print("CHARACTER RANKS (word): ", word_char_ranks)
    # print("CHARACTER RANKS (total): ", total_char_ranks)

    double_sorted_char_ranks = get_best_char_ranks(word_character_counts, total_character_counts)
    word_ranks = create_word_ranks(double_sorted_char_ranks, available_words)
    sorted_words = sort_words_by_rank(word_ranks)
    return list(sorted_words.keys())


def create_word_ranks(total_char_ranks, available_words):
    word_ranks = dict()
    for word in available_words:
        word_char_set = set(word)
        rank = 0
        for char in word_char_set:
            rank += total_char_ranks[char]
        word_ranks[word] = rank

    return word_ranks


def sort_words_by_rank(word_ranks):
    return dict(sorted(word_ranks.items(), key=lambda item: item[1], reverse=True))


def get_best_char_ranks(character_count_dict1, character_count_dict_2):
    # sort by dict1 first, then sort by dict-2
    character_count_dict1 = dict(
        sorted(character_count_dict1.items(), key=(lambda item: (item[1], character_count_dict_2[item[0]])),
               reverse=True))

    number_of_different_characters = len(character_count_dict1)
    character_ranks = create_rank_list(number_of_different_characters)

    char_list = list(character_count_dict1.keys())

    character_rank_dict = dict()
    for i in range(number_of_different_characters):
        character_rank_dict[char_list[i]] = character_ranks[i]

    return character_rank_dict


def get_char_ranks(character_count_dict):
    number_of_different_characters = len(character_count_dict)
    character_ranks = create_rank_list(number_of_different_characters)

    char_list = list(character_count_dict.keys())

    character_rank_dict = dict()
    for i in range(number_of_different_characters):
        character_rank_dict[char_list[i]] = character_ranks[i]

    return character_rank_dict


def create_rank_list(length):
    return sorted([(i + 1) for i in range(length)], reverse=True)
