#! /usr/bin/env python3
import argparse
import math
from collections import defaultdict


class Day6:
    """ Day 6: Universal Orbit Map """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        orbits = defaultdict(list)
        # Read data input.
        with open(input_file, "r") as input:
            for orbit in input:
                parent, child = orbit.rstrip().split(")")
                orbits[parent].append(child)
        print(f"Nb link: {sum(len(v) for v in orbits)}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 6 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day6(args.input)
