#!/usr/bin/env python3
import argparse


class Day7:
    """ Day 7: Handy Haversacks """
    _BAG = "shiny gold"

    def __init__(self, input_file):
        self._bag_rules = dict()
        self.process(input_file)

    def find_bag(self, color: str) -> int:
        for bag in self._bag_rules[color].keys():
            if bag == self._BAG:
                return 1
            elif bag == "none":
                pass
            else:
                if self.find_bag(bag):
                    return 1
        return 0

    def process(self, input_file):
        with open(input_file, "r") as input:
            for line in input:
                line = line.rstrip()
                rule = line.split(" bags contain ")
                main_bag = rule[0]
                contain = rule[1]\
                    .replace("bags", "bag") \
                    .replace(", ", "") \
                    .replace(".", "") \
                    .split(" bag")
                self._bag_rules[main_bag] = dict()
                for cont in contain:
                    if len(cont) == 0:
                        break
                    elif cont == "no other":
                        self._bag_rules[main_bag]["none"] = 0
                    else:
                        nb, bag = cont.split(" ", 1)
                        self._bag_rules[main_bag][bag] = nb
        bag_nb = 0
        for bag in self._bag_rules.keys():
            if bag == self._BAG:
                continue
            bag_nb += self.find_bag(bag)
        print(f"Part 1: {bag_nb}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day7(args.input)
