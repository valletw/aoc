from enum import IntEnum
from typing import List, Tuple


class StepId(IntEnum):
    S2S = 0     # Seed to Soil.
    S2F = 1     # Soil to Fertiliser.
    F2W = 2     # Fertiliser to Water.
    W2L = 3     # Water to Light.
    L2T = 4     # Light to Temperature.
    T2H = 5     # Temperature to Humidity.
    H2L = 6     # Humidity to Location.


# (DEST, SRC, RANGE)
StepDesc = Tuple[int, int, int]
Step = List[StepDesc]


def parse(puzzle_in: List[str]) -> Tuple[List[int], List[Step]]:
    seeds: List[int] = []
    step_id = -1
    steps: List[Step] = []
    for line in puzzle_in:
        if line.startswith("seeds"):
            # Parse all requested seeds.
            seeds = [int(s) for s in line.split(":")[1].strip().split(" ")]
        elif line.startswith("seed-to-soil") \
                or line.startswith("soil-to-fertilizer") \
                or line.startswith("fertilizer-to-water") \
                or line.startswith("water-to-light") \
                or line.startswith("light-to-temperature") \
                or line.startswith("temperature-to-humidity") \
                or line.startswith("humidity-to-location") \
                or line.startswith("light-to-temperature"):
            # New step find, go to next ID.
            step_id += 1
            steps.append([])
        elif line == "":
            # Empty line, do nothing.
            pass
        else:
            # Extract source, destination and range.
            dest, src, size = [int(d) for d in line.split(" ")]
            steps[step_id].append((dest, src, size))
    return seeds, steps


def find_location(seed: int, steps: List[Step]) -> int:
    step_id = StepId.S2S
    find_src = seed
    while step_id <= StepId.H2L:
        for dest, src, size in steps[step_id]:
            if src <= find_src < (src + size):
                find_src = dest + (find_src - src)
                break
        step_id += 1
    return find_src


def process(puzzle_in: List[str]):
    seeds, steps = parse(puzzle_in)
    locations: List[int] = [find_location(seed, steps) for seed in seeds]
    print(f"Part 1: {min(locations)}")
