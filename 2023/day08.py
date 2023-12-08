from math import lcm
from typing import List, Tuple, Dict


Steps = List[int]
Plan = Dict[str, List[str]]


def parse(puzzle_in: List[str]) -> Tuple[Steps, Plan]:
    steps: Steps = []
    plan: Plan = {}
    for line in puzzle_in:
        if line == "":
            continue
        if len(steps) == 0:
            steps = [1 if s == 'R' else 0 for s in line]
        else:
            key, value = line.split("=")
            plan[key.strip()] = value\
                .replace("(", "") \
                .replace(")", "") \
                .replace(",", "") \
                .split()
    return steps, plan


def navigate(steps: Steps, plan: Plan, start: str, end_condition) -> int:
    count = 0
    idx = 0
    pos = start
    while not end_condition(pos):
        count += 1
        pos = plan[pos][steps[idx]]
        idx = (idx + 1) % len(steps)
    return count


def navigate_ghost(steps: Steps, plan: Plan) -> int:
    # Find all starts.
    starts = [s for s in plan if s[-1] == 'A']
    # Count the number of steps to arrived at the end.
    counts: List[int] = [
        navigate(steps, plan, s, lambda p: p[-1] == "Z") for s in starts
    ]
    # Find the commun multiplier for each ways.
    return lcm(*counts)


def process(puzzle_in: List[str]):
    steps, plan = parse(puzzle_in)
    print(f"Part 1: {navigate(steps, plan, 'AAA', lambda p: p == 'ZZZ')}")
    print(f"Part 2: {navigate_ghost(steps, plan)}")
