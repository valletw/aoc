#!/usr/bin/env python3
import argparse
from typing import Dict, Any, List
from day01 import process as d01
from day02 import process as d02
from day03 import process as d03
from day04 import process as d04
from day05 import process as d05
from day06 import process as d06
from day07 import process as d07
from day08 import process as d08
from day09 import process as d09
from day10 import process as d10
from day11 import process as d11
from day12 import process as d12
from day14 import process as d14
from day15 import process as d15
from day18 import process as d18


process: Dict[int, Any] = {
    1: d01,
    2: d02,
    3: d03,
    4: d04,
    5: d05,
    6: d06,
    7: d07,
    8: d08,
    9: d09,
    10: d10,
    11: d11,
    12: d12,
    14: d14,
    15: d15,
    18: d18,
}


def read_puzzle_input(path: str) -> List[str]:
    puzzle_in: List[str] = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            puzzle_in.append(line.rstrip())
    return puzzle_in


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", type=int, required=True,
                        help="Day to execute")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    if args.day in process:
        process[args.day](read_puzzle_input(f"day{args.day:02d}-input.txt"))
    else:
        print("Day not found")
