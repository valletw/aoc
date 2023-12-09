from typing import List


History = List[int]


def parse(puzzle_in: List[str]) -> List[History]:
    sensors: List[History] = []
    for line in puzzle_in:
        sensors.append([int(d) for d in line.split()])
    return sensors


def find_complement(hist: History) -> int:
    # If all zero, end of completion.
    if all(h == 0 for h in hist):
        return 0
    # Compute difference between each elements.
    diffs = [j - i for i, j in zip(hist, hist[1:])]
    # Get last element and add it to the next last difference value.
    return hist[-1] + find_complement(diffs)


def process(puzzle_in: List[str]):
    sensors = parse(puzzle_in)
    print(f"Part 1: {sum(find_complement(s) for s in sensors)}")
    print(f"Part 2: {sum(find_complement(s[::-1]) for s in sensors)}")
