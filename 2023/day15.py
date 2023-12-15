from typing import List


def parse(puzzle_in: List[str]) -> List[str]:
    sequences: List[str] = []
    for line in puzzle_in:
        sequences.extend(line.split(","))
    return sequences


def hash_algo(sequence: str) -> int:
    count = 0
    for c in sequence:
        count += ord(c)
        count *= 17
        count %= 256
    return count


def process(puzzle_in: List[str]):
    sequences = parse(puzzle_in)
    print(f"Part 1: {sum(hash_algo(s) for s in sequences)}")
