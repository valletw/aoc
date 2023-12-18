from enum import IntEnum
from typing import List, Dict, Tuple, Set


# (ROW, COL)
Position = Tuple[int, int]
Mirrors = Dict[Position, str]
Beams = Set[Position]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def parse(puzzle_in: List[str]) -> Tuple[int, int, Mirrors]:
    mirrors: Mirrors = {}
    for row, line in enumerate(puzzle_in):
        for col, c in enumerate(line):
            if c in ['/', '\\', '-', '|']:
                mirrors[(row, col)] = c
    return len(puzzle_in), len(puzzle_in[0]), mirrors


def energize(rmax: int, cmax: int, mirrors: Mirrors) -> Beams:
    beams: Beams = set()
    beams_prev = -1
    positions: List[Tuple[Position, Direction]] = [((0, 0), Direction.RIGHT)]
    while len(beams) != beams_prev:
        beams_prev = len(beams)
        for pos, dir in positions:
            # Get all mirrors on the row.
            if dir in [Direction.LEFT, Direction.RIGHT]:
                mir = { (k, v) for k, v in mirrors.items() if v[0] == pos[0] }
            # Get all mirrors on the column.
            elif dir in [Direction.UP, Direction.DOWN]:
                mir = { (k, v) for k, v in mirrors.items() if v[1] == pos[1] }
            print(mir)
    return beams


def process(puzzle_in: List[str]):
    rmax, cmax, mirrors = parse(puzzle_in)
    print(f"Part 1: {len(energize(rmax, cmax, mirrors))}")
