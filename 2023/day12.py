import re
from typing import List, Tuple


# (REGEX, CONDITION)
Spring = Tuple[str, List[int]]


def parse(puzzle_in: List[str]) -> List[Spring]:
    springs: List[Spring] = []
    for line in puzzle_in:
        rec, cond = line.split()
        springs.append((rec, [int(c) for c in cond.split(",")]))
    return springs


def gen_combinaison(records: List[str], remaining: int) -> str:
    if remaining == 0:
        return records
    new_records: List[str] = []
    # Replace first ? match and move to next call.
    for rec in records:
        new_records.append(rec.replace("?", ".", 1))
        new_records.append(rec.replace("?", "#", 1))
    return gen_combinaison(new_records, remaining - 1)


def count_match(spring: Spring) -> int:
    rec, cond = spring
    # Compute regex to match combinaisons.
    comb_str = "^\\.*"
    for c in cond:
        comb_str += f"#{{{c}}}\\.+"
    comb_str = comb_str[:-3] + "\\.*$"
    comb_re = re.compile(comb_str)
    # Compute every possible combinaisons
    combinaisons = gen_combinaison([rec], rec.count("?"))
    # Sum if combinaison match regex.
    return sum(
        1 if comb_re.match(c) is not None else 0
        for c in combinaisons
    )


def springs_update(springs: List[Spring]) -> List[Spring]:
    new_springs: List[Spring] = []
    for r, c in springs:
        # Complete record with separator.
        r += "?"
        r = r * 5
        new_springs.append((r[:-1], c * 5))
    return new_springs


def process(puzzle_in: List[str]):
    springs = parse(puzzle_in)
    print(f"Part 1: {sum(count_match(s) for s in springs)}")
    # Brute force...
    springs_2 = springs_update(springs)
    print(f"Part 2: {sum(count_match(s) for s in springs_2)}")
