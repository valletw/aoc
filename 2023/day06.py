from operator import mul
from functools import reduce
from typing import List, Tuple


# (TIME, DISTANCE)
RaceDesc = Tuple[int, int]


def parse(puzzle_in: List[str]) -> Tuple[List[RaceDesc], RaceDesc]:
    races: List[RaceDesc] = []
    race_2: RaceDesc = (0, 0)
    time: List[int] = []
    distance: List[int] = []
    for line in puzzle_in:
        if line.startswith("Time"):
            values = line.split(":")[1]
            time = [int(i) for i in values.split()]
            race_2 = (int(values.replace(" ", "")), race_2[1])
        elif line.startswith("Distance"):
            values = line.split(":")[1]
            distance = [int(i) for i in values.split()]
            race_2 = (race_2[0], int(values.replace(" ", "")))
    races.extend((time[i], distance[i]) for i in range(0, len(time)))
    return races, race_2


def get_distance(hold: int, time_max: int) -> int:
    return (time_max - hold) * hold


def record_ways(time_max: int, record: int) -> int:
    match_1 = 0
    match_2 = 0
    # Find first record match from the beginning.
    count = 0
    distance = 0
    while distance <= record:
        count += 1
        distance = get_distance(count, time_max)
    match_1 = count
    # Find last record match from the end.
    count = time_max
    distance = 0
    while distance <= record:
        count -= 1
        distance = get_distance(count, time_max)
    match_2 = count
    # Difference is the number of ways for the record.
    return match_2 - match_1 + 1


def process(puzzle_in: List[str]):
    races, race_2 = parse(puzzle_in)
    records_1: List[int] = []
    # Parse all races (part 1).
    for t, r in races:
        records_1.append(record_ways(t, r))
    print(f"Part 1: {reduce(mul, records_1, 1)}")
    print(f"Part 2: {record_ways(*race_2)}")
