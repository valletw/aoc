#! /usr/bin/env python3
import argparse


class Day24:
    """ Day 24: Planet of Discord """
    def __init__(self, input_file):
        self.bugs = Bugs(input_file)
        self.process()

    def process(self):
        bugs_biodiveristy = set()
        while True:
            bio = self.bugs.biodiversity()
            if bio not in bugs_biodiveristy:
                bugs_biodiveristy.add(bio)
                self.bugs.exec()
            else:
                break
        print(f"Biodiversity: {self.bugs.biodiversity()}")


class Bugs:
    def __init__(self, input_file):
        self.bugs = set()
        self.width = 0
        self.height = 0
        with open(input_file, "r") as input:
            for line in input:
                self.width = 0
                for c in line.rstrip():
                    if c == '#':
                        self.bugs.add((self.width, self.height))
                    self.width += 1
                self.height += 1

    def exec(self):
        new_bugs = set()
        for y in range(self.height):
            for x in range(self.width):
                results = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                results = filter(self.in_bound, results)
                results = filter(self.is_bugs, results)
                nb_bugs = sum(1 for _ in results)
                # It's a bug, die unless exactly one bug adjacent.
                if (x, y) in self.bugs and nb_bugs == 1:
                    new_bugs.add((x, y))
                # It's an empty space, infected if 1 or 2 bugs bugs adjacent.
                elif (x, y) not in self.bugs and nb_bugs in [1, 2]:
                    new_bugs.add((x, y))
        self.bugs = new_bugs

    def is_bugs(self, a):
        return a in self.bugs

    def in_bound(self, a):
        x, y = a
        return 0 <= x < self.width and 0 <= y < self.height

    def biodiversity(self):
        b = 0
        for bug in self.bugs:
            x, y = bug
            b += 2 ** (x + y * self.height)
        return b

    def print(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.bugs:
                    s += str("#")
                else:
                    s += str(".")
            s += str("\n")
        print(s)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 24 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day24(args.input)
