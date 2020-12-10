#!/usr/bin/env python3
import argparse


class Day10:
    """ Day 10: Adapter Array """

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                data.append(int(line))
        adapters = sorted(data)
        adapters.insert(0, 0)
        adapters.append(adapters[-1] + 3)
        differences = list()
        for idx in range(len(adapters) - 1):
            differences.append(adapters[idx + 1] - adapters[idx])
        print(f"Part 1: {differences.count(1) * differences.count(3)}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day10(args.input)
