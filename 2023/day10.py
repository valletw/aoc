from enum import Enum
from typing import List, Tuple, Dict, Optional


Position = Tuple[int, int]


def position_add(p0: Position, p1: Position) -> Position:
    return tuple(map(lambda i, j: i + j, p0, p1))


def position_sub(p0: Position, p1: Position) -> Position:
    return tuple(map(lambda i, j: i - j, p0, p1))


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    @staticmethod
    def convert(pos: Position):
        for d in Direction:
            if pos == d.value:
                return d
        assert False


# (TILES, [MOVE_1, MOVE_2])
class Pipe(Enum):
    # Norht / South.
    NS = ('|', [Direction.NORTH, Direction.SOUTH])
    # East / West.
    EW = ('-', [Direction.EAST, Direction.WEST])
    # North / East 90.
    NE = ('L', [Direction.NORTH, Direction.EAST])
    # North / West 90.
    NW = ('J', [Direction.NORTH, Direction.WEST])
    # South / West 90.
    SW = ('7', [Direction.SOUTH, Direction.WEST])
    # South / East 90.
    SE = ('F', [Direction.SOUTH, Direction.EAST])

    def tile(self) -> str:
        return self.value[0]

    def move(self, pos: Position) -> List[Position]:
        return [
            position_add(pos, m.value) for m in self.value[1]
        ]


Pipes = Dict[Pipe, List[Position]]


def parse(puzzle_in: List[str]) -> Tuple[Position, Pipes, int, int]:
    pipes: Pipes = {}
    pipes[Pipe.NS] = []
    pipes[Pipe.EW] = []
    pipes[Pipe.NE] = []
    pipes[Pipe.NW] = []
    pipes[Pipe.SW] = []
    pipes[Pipe.SE] = []
    start = (0, 0)
    for row in range(0, len(puzzle_in)):
        line = puzzle_in[row]
        for col in range(0, len(line)):
            c = line[col]
            if c == Pipe.NS.tile():
                pipes[Pipe.NS].append((row, col))
            elif c == Pipe.EW.tile():
                pipes[Pipe.EW].append((row, col))
            elif c == Pipe.NE.tile():
                pipes[Pipe.NE].append((row, col))
            elif c == Pipe.NW.tile():
                pipes[Pipe.NW].append((row, col))
            elif c == Pipe.SW.tile():
                pipes[Pipe.SW].append((row, col))
            elif c == Pipe.SE.tile():
                pipes[Pipe.SE].append((row, col))
            elif c == 'S':
                start = (row, col)
    return start, pipes, len(puzzle_in), len(puzzle_in[0])


def scan(start: int, pipes: Pipes, row_max: int, col_max: int) -> int:
    def _get_next_position(
            pos: Position, row_max: int, col_max: int) -> List[Position]:
        # Compute each positions around the current one.
        next_pos = [
            position_add(pos, Direction.NORTH.value),
            position_add(pos, Direction.EAST.value),
            position_add(pos, Direction.SOUTH.value),
            position_add(pos, Direction.WEST.value)
        ]
        # Remove positions out of range.
        return list(filter(
            lambda p: -1 not in p and p[0] < row_max and p[1] < col_max,
            next_pos))

    def _get_move(
            pos: Position, direction: Direction,
            pipes: Pipes) -> Optional[Pipe]:
        # Check for pipe element for corresponding direction.
        # Note: thing in opposite dirrection => "input from" and "output to".
        if direction == Direction.NORTH:
            if pos in pipes[Pipe.NS]:
                return Pipe.NS
            if pos in pipes[Pipe.SE]:
                return Pipe.SE
            if pos in pipes[Pipe.SW]:
                return Pipe.SW
        elif direction == Direction.EAST:
            if pos in pipes[Pipe.EW]:
                return Pipe.EW
            if pos in pipes[Pipe.NW]:
                return Pipe.NE
            if pos in pipes[Pipe.SW]:
                return Pipe.SE
        elif direction == Direction.SOUTH:
            if pos in pipes[Pipe.NS]:
                return Pipe.NS
            if pos in pipes[Pipe.NE]:
                return Pipe.NE
            if pos in pipes[Pipe.NW]:
                return Pipe.NW
        elif direction == Direction.WEST:
            if pos in pipes[Pipe.EW]:
                return Pipe.EW
            if pos in pipes[Pipe.NE]:
                return Pipe.NW
            if pos in pipes[Pipe.SE]:
                return Pipe.SW
        return None

    # Compute first positions from start.
    positions: List[Tuple[Position, Position]] = []
    for np in _get_next_position(start, row_max, col_max):
        # Compute direction.
        direction = Direction.convert(position_sub(np, start))
        # Get potential pipe.
        move = _get_move(np, direction, pipes)
        if move is not None:
            positions.append((
                list(filter(lambda m: m != start, move.move(np)))[0],
                np
            ))
    # Iterate until positions join again.
    assert len(positions) == 2
    count = 2
    while positions[0][0] != positions[1][0]:
        for i in range(0, 2):
            pos, prev_pos = positions[i]
            # Compute direction.
            direction = Direction.convert(position_sub(pos, prev_pos))
            # Get potential pipe.
            move = _get_move(pos, direction, pipes)
            assert move is not None
            # Update current position.
            positions[i] = (
                list(filter(lambda m: m != prev_pos, move.move(pos)))[0],
                pos
            )
        count += 1
    return count


def process(puzzle_in: List[str]):
    start, pipes, rmax, cmax = parse(puzzle_in)
    print(f"Part 1: {scan(start, pipes, rmax, cmax)}")
