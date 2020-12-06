#!/usr/bin/env python3
import argparse


class Day6:
    """ Day 5: Custom Customs """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        question_list = [chr(c) for c in range(0x61, 0x7B)]
        groups_1 = list()
        groups_2 = list()
        group_id = 0
        groups_1.append(set())
        groups_2.append({"nb": 0, "raw": ""})
        with open(input_file, "r") as input:
            for line in input:
                line = line.rstrip()
                if line == "":
                    group_id += 1
                    groups_1.append(set())
                    groups_2.append({"nb": 0, "raw": ""})
                else:
                    for response in line:
                        groups_1[group_id].add(response)
                    groups_2[group_id]["nb"] += 1
                    groups_2[group_id]["raw"] += line
        response_nb_1 = sum(len(resp) for resp in groups_1)
        response_nb_2 = sum(g["raw"].count(c) == g["nb"] for c in question_list for g in groups_2)
        print(f"Part 1: {response_nb_1}")
        print(f"Part 2: {response_nb_2}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day6(args.input)
