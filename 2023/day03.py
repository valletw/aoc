import re
from typing import List, Set, Tuple


# (ROW, COL)
Position = Tuple[int, int]
# (ROW, COL, LEN, VALUE)
NumberDesc = Tuple[int, int, int, int]


def find_number_and_symbols(
        puzzle_in: List[str]) -> Tuple[Set[NumberDesc], Set[Position]]:
    numbers: Set[NumberDesc] = set()
    symbols: Set[Position] = set()
    # Parse each line to find a symbol, and store the position.
    col_max = len(puzzle_in[0])
    row = 0
    for line in puzzle_in:
        col = 0
        while col < col_max:
            c = line[col]
            # It is a digit => add it to the list, and skip next column.
            if c.isdigit():
                number = re.split(r"\D+", line[col:])[0]
                num_size = len(number)
                numbers.add((row, col, num_size, int(number)))
                col += num_size
            # Not a digit and not a dot => symbol.
            elif c != ".":
                symbols.add((row, col))
                col += 1
            else:
                col += 1
        row += 1
    return numbers, symbols


def compute_boundaries(row: int, col: int, len_s: int) -> Set[Position]:
    boundaries: Set[Position] = set()
    # Column before & after and number length.
    for rc in range(col - 1, col + len_s + 1):
        # Row up & down.
        for rr in range(row - 1, row + 2):
            boundaries.add((rr, rc))
    return boundaries


def dump(
        row_max: int, col_max: int, numbers: List[NumberDesc],
        symbols: List[Position]):
    p_num = 0
    for row in range(0, row_max):
        for col in range(0, col_max):
            if p_num > 0:
                p_num -= 1
                if p_num != 0:
                    continue
            if (row, col) in symbols:
                print("*", end="")
            else:
                for num in numbers:
                    if row == num[0] and col == num[1]:
                        print(f"{num[3]}", end="")
                        p_num = num[2]
                if p_num == 0:
                    print(".", end="")
        print("")


def process(puzzle_in: List[str]):
    # Extract numbers and symbols.
    numbers, symbols = find_number_and_symbols(puzzle_in)
    # Parse numbers and check if symbol is close to it.
    adjacents: List[int] = []
    for number in numbers:
        # Get boundaries.
        boundaries = compute_boundaries(number[0], number[1], number[2])
        # It is a partno for any symbols in boundaries.
        if any(i in symbols for i in boundaries):
            adjacents.append(number[3])
    print(f"Part 1: {sum(adjacents)}")
