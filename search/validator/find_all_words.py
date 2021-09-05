"Takes a grid of letters and searches for valid words"
import gzip
import time
from collections import deque
from multiprocessing import Pool
from sys import argv
from typing import List, NamedTuple, Set


class Index(NamedTuple):
    column: int
    row: int


class IndexAndLevel(NamedTuple):
    index: Index
    level: int


def make_word_set(file_path: str) -> Set[str]:
    words = set()
    with gzip.open(file_path, "r") as all_words:
        for word in all_words:
            words.add(word.strip().decode("utf-8"))
    return words


def get_valid_prefixes(file_path: str) -> Set[str]:
    prefixes = set()
    with open(file_path) as calculated_prefixes:
        for word_line in calculated_prefixes:
            prefixes.add(word_line.strip())
    return prefixes


def find_sequences_at_anchor(letter_grid: List[List [str]],
                             anchor_index: Index,
                             max_word_length: int = 14,
                             prefixes: Set[str] = None,
                             ) -> List[str]:
    if len(letter_grid) < 1 or len(letter_grid[0]) < 1:
        raise ValueError("The grid of letters must be at least 1x1")
    max_columns = len(letter_grid)
    max_rows = len(letter_grid[0])
    index_stack = deque()
    index_stack.append(IndexAndLevel(anchor_index, 1))
    current_word = ""
    word_list = []
    searched_indices = []
    if prefixes:
        prefix_elem = prefixes.pop()
        prefixes.add(prefix_elem)
    while index_stack:
        index = index_stack.pop()
        searched_indices = searched_indices[: index.level - 1] + [index.index]
        current_word = current_word[: index.level - 1] + \
                       letter_grid[index.index.column][index.index.row]
        if len(current_word) > 2:
            word_list.append(current_word)
        if index.level < max_word_length and \
                (not prefixes or len(current_word) != len(prefix_elem) or current_word in prefixes):
            neighbors = add_neighbors(max_columns,
                                      max_rows,
                                      index.index.column,
                                      index.index.row,
                                      searched_indices)
            for neighbor in neighbors:
                index_stack.append(IndexAndLevel(neighbor, index.level + 1))

    return word_list


def get_all_words(sequences: List[str], valid_words: Set[str]) -> List[str]:
    return [word for word in sequences if word in valid_words]


def find_all_words_at_anchor(letter_grid: List[List [str]],
                             anchor_index: Index,
                             valid_words: Set[str],
                             prefixes: Set[str] = None) -> List[str]:
    return get_all_words(find_sequences_at_anchor(letter_grid, anchor_index, prefixes=prefixes), valid_words)


def add_neighbors(max_columns: int,
                  max_rows: int,
                  col_index: int,
                  row_index: int,
                  searched_indices: Set[Index]) -> List[Index]:
    new_indices = [Index(col_index - 1, row_index - 1),
                   Index(col_index, row_index - 1),
                   Index(col_index + 1, row_index - 1),
                   Index(col_index + 1, row_index),
                   Index(col_index + 1, row_index + 1),
                   Index(col_index, row_index + 1),
                   Index(col_index - 1, row_index + 1),
                   Index(col_index - 1, row_index)]
    return list(filter(lambda x: x not in searched_indices,
                       filter(lambda i: 0 <= i.column < max_columns and \
                                        0 <= i.row < max_rows,
                              new_indices)))


def make_grid_from_string_input(characters: str) -> List[List[str]]:
    character_list = list(characters)
    if "," in characters:
        character_list = characters.split(",")
    if len(character_list) != 16:
        raise ValueError("The input must make a 4x4 grid. This list is %i" % len(character_list))
    return [character_list[0:4],
            character_list[4:8],
            character_list[8:12],
            character_list[12:16]]


if __name__ == "__main__":
    start_time = time.time()
    found_words = set()
    indices = [Index(0, 0), Index(0, 1), Index(0, 2), Index(0, 3),
               Index(1, 0), Index(1, 1), Index(1, 2), Index(1, 3),
               Index(2, 0), Index(2, 1), Index(2, 2), Index(2, 3),
               Index(3, 0), Index(3, 1), Index(3, 2), Index(3, 3)]
    grid = make_grid_from_string_input(argv[1])
    valid_words = make_word_set("lowercase_words.txt.gz")
    prefixes = get_valid_prefixes("prefix_length_4.txt")
    inputs = [(grid, i, valid_words, prefixes) for i in indices]
    values = []
    with Pool(processes=5) as pool:
        values = values + pool.starmap(find_all_words_at_anchor, inputs)
    for i in range(len(indices)):
        print(f"\nFor index {indices[i]}:")
        for word in values[i]:
            if word not in found_words:
                print(word)
                found_words.add(word)
    print(f"Solved board in {time.time() - start_time} seconds.")
    print(f"Found {len(found_words)} words.")
