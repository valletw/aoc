#!/usr/bin/env python3
import argparse
import math


class Day5:
    """ Day 5: Binary Boarding """
    _ROW_MAX = 128
    _COL_MAX = 8

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        partition = list()
        with open(input_file, "r") as input:
            for line in input:
                partition.append(line.rstrip())
        highest_seat_id = 0
        for part in partition:
            seat_id = self.get_seat_id(*self.get_position(part))
            if seat_id > highest_seat_id:
                highest_seat_id = seat_id
        print(f"Part 1: {highest_seat_id}")

    def get_seat_id(self, row, col) -> int:
        return row * 8 + col

    def get_position(self, partition: str) -> (int, int):
        row_min = 0
        row_max = self._ROW_MAX - 1
        col_min = 0
        col_max = self._COL_MAX - 1
        # Parse rows partitioning.
        for p in partition[0:7]:
            if p == "F":
                row_max = row_min + math.floor((row_max - row_min) / 2)
            elif p == "B":
                row_min = row_min + math.ceil((row_max - row_min) / 2)
            else:
                raise ValueError
        # Parse columns partitioning.
        for p in partition[7:]:
            if p == "L":
                col_max = col_min + math.floor((col_max - col_min) / 2)
            elif p == "R":
                col_min = col_min + math.ceil((col_max - col_min) / 2)
            else:
                raise ValueError
        return row_min, col_min


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day5(args.input)
