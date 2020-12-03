#!/usr/bin/env python3
import argparse


class Day3:
    """ Day 3: Toboggan Trajectory """
    _MOVE = [
        (3, 1), (1, 1), (5, 1), (7, 1), (1, 2)
    ]

    def __init__(self, input_file):
        self._trees = set()
        self._x_max = 0
        self._y_max = 0
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            for line_idx, line in enumerate(input):
                for char_idx, char in enumerate(line.rstrip()):
                    if char == "#":
                        self._trees.add((char_idx, line_idx))
                    self._x_max = char_idx + 1
                self._y_max = line_idx + 1
        part1_done = False
        nb_tree_crossed_1 = 0
        nb_tree_crossed_2 = 1
        for mx, my in self._MOVE:
            x = 0
            y = 0
            nb_tree_crossed = 0
            while y < self._y_max:
                x += mx
                y += my
                nb_tree_crossed += self.is_tree(x, y)
            if not part1_done:
                part1_done = True
                nb_tree_crossed_1 = nb_tree_crossed
            nb_tree_crossed_2 *= nb_tree_crossed
        print(f"Part 1: {nb_tree_crossed_1}")
        print(f"Part 2: {nb_tree_crossed_2}")

    def is_tree(self, x, y):
        xn = x % self._x_max
        return (xn, y) in self._trees


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day3(args.input)
