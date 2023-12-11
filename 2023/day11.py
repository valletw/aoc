from typing import List, Set, Tuple


# (ROW, COL)
Position = Tuple[int, int]


def parse(puzzle_in: List[str]) -> Tuple[Set[Position], int, int]:
    galaxies: Set[Position] = set()
    for row in range(0, len(puzzle_in)):
        line = puzzle_in[row]
        for col in range(0, len(line)):
            if line[col] == '#':
                galaxies.add((row, col))
    return galaxies, len(puzzle_in), len(puzzle_in[0])


def cosmic_expansion(
        galaxies: Set[Position], row_max: int, col_max: int) -> Set[Position]:
    def _expand(galaxies: Set[Position], set_id: int, pmax: int) -> List[int]:
        count = [
            len(list(filter(lambda g: g[set_id] == i, galaxies)))
            for i in range(0, pmax)
        ]
        exp: List[int] = []
        exp_count = 0
        for c in count:
            if c == 0:
                exp_count += 1
            exp.append(exp_count)
        return exp

    galaxies_expanded: Set[Position] = set()
    row_exp = _expand(galaxies, 0, row_max)
    col_exp = _expand(galaxies, 1, col_max)
    for row in range(0, row_max):
        for col in range(0, col_max):
            if (row, col) in galaxies:
                galaxies_expanded.add((row + row_exp[row], col + col_exp[col]))
    return galaxies_expanded


def distances(galaxies: Set[Position]) -> List[Tuple[int, Position, Position]]:
    dist: List[Tuple[int, Position, Position]] = []
    passed: Set[Position] = set()
    for g0 in galaxies:
        passed.add(g0)
        for g1 in galaxies ^ passed:
            distance = abs(g0[0] - g1[0]) + abs(g0[1] - g1[1])
            dist.append((distance, g0, g1))
    return dist


def dump(galaxies: Set[Position], row_max: int, col_max: int):
    for row in range(0, row_max):
        for col in range(0, col_max):
            if (row, col) in galaxies:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def process(puzzle_in: List[str]):
    galaxies = cosmic_expansion(*parse(puzzle_in))
    print(f"Part 1: {sum(d[0] for d in distances(galaxies))}")
