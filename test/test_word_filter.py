import string

import pytest

import wordle_helper.word_filter as word_filter


def test_get_top_five_most_common_characters(alphabet_count_dict):
    all_words_list = ["ab", "abcde", "a"]
    top_5 = word_filter.get_top_five_most_common_characters(all_words_list)

    expected = alphabet_count_dict.copy()
    expected['a'] = 3
    expected['b'] = 2
    expected['c'] = 1
    expected['d'] = 1
    expected['e'] = 1
    assert expected == top_5

    all_words_list = []
    top_5 = word_filter.get_top_five_most_common_characters(all_words_list)
    expected = alphabet_count_dict.copy()
    assert expected == top_5


@pytest.fixture()
def alphabet_count_dict():
    return dict.fromkeys(string.ascii_lowercase, 0)


def test_find_words_with_characters_for_guesses_out_of_place():
    words = ["worda", "wordb", "abcde"]
    guesses = []

    result = word_filter.filter_words_by_characters_out_of_place(words.copy(), guesses)
    assert result == words

    guesses = ["____a, ____b"]
    expected = ["abcde"]
    result = word_filter.filter_words_by_characters_out_of_place(words.copy(), guesses)
    assert result == expected


def test_get_chars_from_guesses():
    guesses = ["__r_c", "r_a_s"]
    result = word_filter.get_chars_from_guesses(guesses)
    expected = ['a', 'c', 'r', 's']
    assert result == expected


def test_filter_words_containing_characters():
    words = ["homes", "docks", "tests"]
    guesses = ["se___", "__moh"]

    expected = ["homes"]
    result = word_filter.filter_words_containing_characters(words, guesses)
    assert expected == result


def test_create_guess_char_indices_dict():
    guesses = ["a____", "_b___", "____c", "c____"]

    result = word_filter.create_guess_char_indices_dict(guesses)
    expected = {'a': [0], 'b': [1], 'c': [0, 4]}

    assert result == expected
