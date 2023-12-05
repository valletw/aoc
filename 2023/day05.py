import multiprocessing as mp
from enum import IntEnum
from typing import List, Tuple


NB_THREAD = 8


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


def parse(puzzle_in: List[str]) -> Tuple[
        List[int], List[Tuple[int, int]], List[Step]]:
    seeds_1: List[int] = []
    seeds_2: List[Tuple[int, int]] = []
    step_id = -1
    steps: List[Step] = []
    for line in puzzle_in:
        if line.startswith("seeds"):
            # Parse all requested seeds.
            seeds_1 = [int(s) for s in line.split(":")[1].strip().split(" ")]
            seeds_2 = list(zip(seeds_1[0::2], seeds_1[1::2]))
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
    return seeds_1, seeds_2, steps


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


def find_location_process(q, seed_s: int, seed_r: int, steps: List[Step]):
    seed_id = seed_s
    seed_end = seed_s + seed_r
    vmin = 0xffffffffffffffff
    while seed_id <= seed_end:
        if seed_id % 1000000 == 0:
            print(".", end="", flush=True)
        vmin = min(vmin, find_location(seed_id, steps))
        seed_id += 1
    q.put(vmin)


def process(puzzle_in: List[str]):
    seeds_1, seeds_2, steps = parse(puzzle_in)
    locations: List[int] = [find_location(seed, steps) for seed in seeds_1]
    print(f"Part 1: {min(locations)}")
    # Brute force mode...
    locations_bf: List[int] = []
    mp.set_start_method('spawn')
    for seed_min, seed_size in seeds_2:
        queues = []
        proc = []
        chunk = int(seed_size / NB_THREAD) + 1
        seed = seed_min
        # Create each threads and start them.
        for _ in range(0, NB_THREAD):
            seed_end = seed + chunk
            if seed_end > seed_min + seed_size:
                seed_end = seed_min + seed_size
            queues.append(mp.Queue())
            proc.append(mp.Process(
                target=find_location_process,
                args=(queues[-1], seed, seed_end, steps)))
            proc[-1].start()
            seed += chunk
        # Wait all threads and get minimal value.
        for i in range(0, NB_THREAD):
            locations_bf.append(queues[i].get())
            proc[i].join()
        print("")
    print(f"Part 2: {min(locations_bf)}")
