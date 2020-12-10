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
        permutations_factor = [0, 0, 2, 4, 7]
        permutations = list()
        count = 0
        for diff in differences:
            if diff == 1:
                count += 1
            else:
                if count > 1:
                    permutations.append(count)
                count = 0
        ways = 1
        for p in permutations:
            ways *= permutations_factor[p]
        print(f"Part 1: {differences.count(1) * differences.count(3)}")
        print(f"Part 2: {ways}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day10(args.input)
