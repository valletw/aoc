from typing import List, Tuple, Dict


# (ROW, COL)
Position = Tuple[int, int]
# (DIRECTION, LENGTH, COLOR)
Plan = List[Tuple[str, int, int]]


def parse(puzzle_in: List[str]) -> Plan:
    plan: Plan = []
    for line in puzzle_in:
        direction, length, color_s = line.split()
        plan.append((direction, int(length), int(color_s[2:-1], 16)))
    return plan


def dig(plan: Plan) -> Tuple[List[Position], int]:
    dirs: Dict[str, Position] = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1)
    }
    pos = (0, 0)
    corners: List[Position] = []
    edges = 0
    # Parse each plan instruction.
    for D, L, _ in plan:
        # Compute new corner.
        end = tuple(a + L * b for a, b in zip(pos, dirs[D]))
        edges += L
        corners.append(end)
        pos = end
    return corners, edges


def area(corners: List[Position], edges: int) -> int:
    # Check Shoelace formula & Pick's theorem.
    r = 0
    for i in range(len(corners) - 1):
        r1, c1 = corners[i]
        r2, c2 = corners[i + 1]
        r += (c1 * r2) - (c2 * r1)
    return (abs(r) // 2) + (edges // 2) + 1


def dump(trench: List[Position]):
    row_sort = sorted(trench)
    rmin = row_sort[0][0]
    rmax = row_sort[-1][0] + 1
    col_sort = sorted(trench, key=lambda a: a[1])
    cmin = col_sort[0][1]
    cmax = col_sort[-1][1] + 1
    for R in range(rmin, rmax):
        for C in range(cmin, cmax):
            if (R, C) == (0, 0):
                print("X", end="")
            elif (R, C) in trench:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def process(puzzle_in: List[str]):
    plan = parse(puzzle_in)
    print(f"Part 1: {area(*dig(plan))}")
