from search.validator.find_all_words import *


def make_test_grid():
    return [['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 'k', 'l'],
            ['m', 'n', 'o', 'p']]


def test_in_base_case_generate_all_neighbors():
    neighbors = add_neighbors(4, 4, 1, 1, set())
    assert Index(0, 0) in neighbors
    assert Index(1, 0) in neighbors
    assert Index(2, 0) in neighbors
    assert Index(0, 1) in neighbors
    assert Index(2, 1) in neighbors
    assert Index(2, 0) in neighbors
    assert Index(2, 1) in neighbors
    assert Index(2, 2) in neighbors
    assert len(neighbors) == 8


def test_if_upper_left_corner_do_not_add_negative_indices():
    """We should filter out any negative indices"""
    neighbors = add_neighbors(4, 4, 0, 0, set())
    assert Index(-1, -1) not in neighbors
    assert Index(-1, 0) not in neighbors
    assert Index(0, -1) not in neighbors
    assert len(neighbors) == 3


def test_if_lower_right_corner_do_not_add_overflow_indices():
    """We should filter out indices bigger than the grid"""
    neighbors = add_neighbors(4, 4, 3, 3, set())
    assert Index(4, 4) not in neighbors
    assert Index(4, 3) not in neighbors
    assert Index(3, -4) not in neighbors
    assert len(neighbors) == 3


def test_do_not_add_already_searched_indices():
    """We do not want to revisit indices"""
    visited = set()
    visited.add(Index(1, 1))
    assert Index(1, 1) not in add_neighbors(4, 4, 0, 0, visited)


def test_find_all_sequences_for_anchor():
    """Happy path test"""
    sequences = find_sequences_at_anchor(make_test_grid(), Index(0, 0), defaultdict(), 3)
    assert sequences == ["abc", "abg", "abf", "abe",
                         "afb", "afc", "afg", "afk", "afj", "afi", "afe",
                         "aeb", "aef", "aej", "aei"]


def test_at_anchor_only_find_valid_words():
    """Only words in the valid set of words get returned"""
    words = find_all_words_at_anchor(make_test_grid(), Index(1, 1), set(["fbcd", "fkn"]),
                                     defaultdict())
    assert words == ["fbcd", "fkn"]