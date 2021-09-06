import gzip
from sys import argv
from typing import List, Set, TextIO


def find_valid_prefixes(word_list: TextIO, prefix_lengths: List[int]) -> Set[str]:
    prefixes = set()
    for word_line in word_list:
        word = word_line.strip().decode("utf-8")
        for length in prefix_lengths:
            if len(word) > length:
                prefixes.add(word[:length])
    return prefixes


if __name__ == "__main__":
    with gzip.open(argv[1], "r") as all_words:
        with open(argv[2], "w") as output:
            for prefix in find_valid_prefixes(all_words, [int(i) for i in argv[3:]]):
                output.write(f"{prefix}\n")