#!/usr/bin/env python3
import argparse


class Day6:
    """ Day 5: Custom Customs """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        groups = list()
        group_id = 0
        groups.append(set())
        with open(input_file, "r") as input:
            for line in input:
                line = line.rstrip()
                if line == "":
                    group_id += 1
                    groups.append(set())
                else:
                    for response in line:
                        groups[group_id].add(response)
        response_nb = sum(len(resp) for resp in groups)
        print(f"Part 1: {response_nb}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day6(args.input)
