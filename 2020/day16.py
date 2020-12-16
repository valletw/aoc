#!/usr/bin/env python3
import argparse


class Day16:
    """ Day 16: Ticket Translation """

    def __init__(self, input_file):
        self._ticket = list()
        self._nearby = list()
        self._rules = dict()
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            nearby = False
            ticket = False
            for line in input:
                line = line.rstrip()
                if line == "your ticket:":
                    ticket = True
                elif line == "nearby tickets:":
                    nearby = True
                elif line == "":
                    pass
                else:
                    if nearby:
                        self._nearby.append([int(f) for f in line.split(",")])
                    elif ticket:
                        self._ticket = [int(f) for f in line.split(",")]
                    else:
                        rule, ranges = line.split(": ")
                        self._rules[rule] = ranges.split(" or ")
        error_rate = 0
        field_unmatch = [[] for _ in range(len(self._ticket))]
        for ticket in self._nearby:
            for idx, field in enumerate(ticket):
                check_success = 0
                for _, (rule, limits) in enumerate(self._rules.items()):
                    for limit in limits:
                        l_min, l_max = [int(l) for l in limit.split("-")]
                        if l_min <= field and field <= l_max:
                            check_success += 1
                        else:
                            field_unmatch[idx].append(rule)
                if check_success == 0:
                    error_rate += field
        #field_unmatch = [sorted(list(set(f))) for f in field_unmatch]
        for idx, unmatch in enumerate(field_unmatch):
            print(idx, unmatch)
        print(f"Part 1: {error_rate}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day16(args.input)
