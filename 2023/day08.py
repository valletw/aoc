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


def navigate(steps: Steps, plan: Plan) -> int:
    count = 0
    idx = 0
    pos = "AAA"
    while pos != "ZZZ":
        count += 1
        pos = plan[pos][steps[idx]]
        idx = (idx + 1) % len(steps)
    return count


def process(puzzle_in: List[str]):
    steps, plan = parse(puzzle_in)
    print(f"Part 1: {navigate(steps, plan)}")
