#!/usr/bin/env python3
import argparse


class Day3:
    """ Day 3: Toboggan Trajectory """
    _MOVE_X = 3
    _MOVE_Y = 1

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
        x = 0
        y = 0
        nb_tree_crossed = 0
        while y < self._y_max:
            x += self._MOVE_X
            y += self._MOVE_Y
            nb_tree_crossed += self.is_tree(x, y)
        print(f"Part 1: {nb_tree_crossed}")

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
