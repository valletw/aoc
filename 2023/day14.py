from typing import List, Tuple, Optional


# (ROW, COL)
Position = Tuple[int, int]
Roundeds = List[Position]
Cubes = List[Position]


def parse(puzzle_in: List[str]) -> Tuple[int, int, Roundeds, Cubes]:
    roundeds: Roundeds = []
    cubes: Cubes = []
    row_max = len(puzzle_in)
    col_max = len(puzzle_in[0])
    for row in range(len(puzzle_in)):
        for col in range(len(puzzle_in[0])):
            if puzzle_in[row][col] == "O":
                roundeds.append((row, col))
            if puzzle_in[row][col] == "#":
                cubes.append((row, col))
    return row_max, col_max, roundeds, cubes


def tilt(row_max: int, col_max: int, roundeds: Roundeds, cubes: Cubes):
    # Parse each lines to ensure first is updated before moving it.
    for row in range(1, row_max):
        for col in range(col_max):
            # Check if it is a rounded rocks.
            if (row, col) in roundeds:
                # Get index in the list.
                idx = roundeds.index((row, col))
                # Get all shapes on the same column.
                up_r = sorted(list(
                    filter(lambda a: a[0] < row and a[1] == col, roundeds)))
                up_c = sorted(list(
                    filter(lambda a: a[0] < row and a[1] == col, cubes)))
                # Cube is found, move to the last one.
                cube_row: Optional[int] = None
                rounded_row: Optional[int] = None
                if len(up_c) != 0:
                    cube_row = up_c[-1][0]
                # Rounded is found, move to the last one.
                if len(up_r) != 0:
                    rounded_row = up_r[-1][0]
                # Update the row.
                if cube_row is not None and rounded_row is not None:
                    roundeds[idx] = (max(cube_row, rounded_row) + 1, col)
                elif rounded_row is not None:
                    roundeds[idx] = (rounded_row + 1, col)
                elif cube_row is not None:
                    roundeds[idx] = (cube_row + 1, col)
                else:
                    roundeds[idx] = (0, col)


def get_load(row_max: int, col_max: int, roundeds: Roundeds, _) -> int:
    load = 0
    for row in range(row_max):
        for col in range(col_max):
            if (row, col) in roundeds:
                load += row_max - row
    return load


def dump(row_max: int, col_max: int, roundeds: Roundeds, cubes: Cubes):
    for row in range(row_max):
        for col in range(col_max):
            pos = (row, col)
            if pos in roundeds:
                print("O", end="")
            elif pos in cubes:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def process(puzzle_in: List[str]):
    parsed = parse(puzzle_in)
    tilt(*parsed)
    print(f"Part 1: {get_load(*parsed)}")
