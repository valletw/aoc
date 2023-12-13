from math import ceil
from typing import List, Tuple
from collections import Counter


Map = List[str]


def parse(puzzle_in: List[str]) -> List[Map]:
    maps: List[Map] = [[]]
    for line in puzzle_in:
        if line == "":
            maps.append([])
        else:
            maps[-1].append(line)
    return maps


def transpose(m: Map) -> Map:
    new: Map = []
    for nm in list(map(list, zip(*m))):
        new.append("".join(nm))
    return new


def find_symetry(m: Map) -> int:
    def _find_middle(diff: List[int]) -> int:
        for d in diff:
            if d != 1:
                return ceil(diff.index(d) / 2)
        return ceil(len(diff) / 2)
    row_count = Counter(m)
    # Only unique lines, no symetry.
    if all(v == 1 for v in row_count.values()):
        return 0
    # Get all line indexes with symetry.
    sym_idx: List[int] = []
    for r in [k for k, v in row_count.items() if v > 1]:
        sym_idx.extend([i for i, e in enumerate(m) if e == r])
    sym_idx.sort()
    diffs = [j - i for i, j in zip(sym_idx, sym_idx[1:])]
    # print(sym_idx, diffs)
    # Check if symetry start from the end.
    if sym_idx[-1] == len(m) - 1 and diffs[-1] == 1:
        mid = _find_middle(list(reversed(diffs)))
        return sym_idx[len(sym_idx) - 1 - mid]
    # Check if symetry start from the begining.
    elif sym_idx[0] == 0 and diffs[0] == 1:
        mid = _find_middle(diffs)
        return sym_idx[mid - 1]
    # Do not start from beginning or end, no symetry.
    return 0


def coordinate(r: int, c: int) -> int:
    if r != 0:
        r += 1
    if c != 0:
        c += 1
    return (r * 100) + c


def process(puzzle_in: List[str]):
    maps = parse(puzzle_in)
    # mid = 3
    # for l in maps[mid]:
    #     print(l)
    # print("")
    # for l in transpose(maps[mid]):
    #     print(l)
    # print("")
    # print(coordinate(find_symetry(maps[mid]), find_symetry(transpose(maps[mid]))))
    coordinates: List[int] = [
        coordinate(find_symetry(m), find_symetry(transpose(m))) for m in maps
    ]
    print(coordinates)
    print(f"Part 1: {sum(coordinates)}")
