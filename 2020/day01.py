#!/usr/bin/env python3
import argparse


class Day1:
    """ Day 1: Report Repair """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data_in = list()
        with open(input_file, "r") as input:
            for d in input:
                data_in.append(int(d))
        for idx, d1 in enumerate(data_in):
            for d2 in data_in[idx + 1:]:
                if d1 + d2 == 2020:
                    print(f"Part1: {d1 * d2}")
                    break


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day1(args.input)
