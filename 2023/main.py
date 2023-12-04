#!/usr/bin/env python3
import argparse
from typing import Dict, Any, List
from day01 import process as d01
from day02 import process as d02
from day04 import process as d04


process: Dict[int, Any] = {
    1: d01,
    2: d02,
    4: d04,
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
