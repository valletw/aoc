#!/usr/bin/env python3
import argparse


class Day15:
    """ Day 15: Rambunctious Recitation """
    _NTH = 2020

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                for n in line.rstrip().split(","):
                    data.append(int(n))
        spoken = data.copy()
        for i in range(self._NTH):
            if i < len(data):
                continue
            if spoken.count(spoken[i - 1]) == 1:
                spoken.append(0)
            else:
                spoken_rev = list(reversed(spoken[0:i - 1]))
                idx = len(spoken_rev) - spoken_rev.index(spoken[i - 1])
                spoken.append(i - idx)
        print(f"Part 1: {spoken[self._NTH - 1]}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day15(args.input)
