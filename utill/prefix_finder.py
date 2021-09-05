import gzip
from sys import argv
from typing import Set, TextIO


def find_valid_prefixes(word_list: TextIO, prefix_length: int) -> Set[str]:
    prefixes = set()
    for word_line in word_list:
        word = word_line.strip().decode("utf-8")
        if len(word) > prefix_length:
            prefixes.add(word[:prefix_length])
    return prefixes


if __name__ == "__main__":
    with gzip.open(argv[1], "r") as all_words:
        with open(argv[3], "w") as output:
            for prefix in find_valid_prefixes(all_words, int(argv[2])):
                output.write(f"{prefix}\n")