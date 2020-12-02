#!/usr/bin/env python3
import argparse


class Day2:
    """ Day 2: Password Philosophy """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data_in = list()
        with open(input_file, "r") as input:
            for line in input:
                group = line.split()
                data_in.append((
                    int(group[0].split("-")[0]),
                    int(group[0].split("-")[1]),
                    group[1].split(":")[0],
                    group[2]))
        match_count_1 = 0
        match_count_2 = 0
        for data in data_in:
            n_min, n_max, char, pw = data
            if n_min <= pw.count(char) and pw.count(char) <= n_max:
                match_count_1 += 1
            if (pw[n_min - 1] == char) + (pw[n_max - 1] == char) == 1:
                match_count_2 += 1
        print(f"Part 1: {match_count_1}")
        print(f"Part 2: {match_count_2}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day2(args.input)
