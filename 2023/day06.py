from operator import mul
from functools import reduce
from typing import List, Tuple


# (TIME, DISTANCE)
RaceDesc = Tuple[int, int]


def parse(puzzle_in: List[str]) -> List[RaceDesc]:
    races: List[RaceDesc] = []
    time: List[int] = []
    distance: List[int] = []
    for line in puzzle_in:
        if line.startswith("Time"):
            time = [int(i) for i in line.split(":")[1].split()]
        elif line.startswith("Distance"):
            distance = [int(i) for i in line.split(":")[1].split()]
    races.extend((time[i], distance[i]) for i in range(0, len(time)))
    return races


def get_distance(hold: int, time_max: int) -> int:
    return (time_max - hold) * hold


def process(puzzle_in: List[str]):
    races = parse(puzzle_in)
    record_ways: List[int] = []
    for t, r in races:
        distances = [get_distance(h, t) for h in range(0, t)]
        record_ways.append(len([d for d in distances if d >= r]))
    print(f"Part 1: {reduce(mul, record_ways, 1)}")
