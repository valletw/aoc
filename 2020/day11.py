#!/usr/bin/env python3
import argparse


class Day11:
    """ Day 11: Seating System """

    def __init__(self, input_file):
        self._x_max = 0
        self._y_max = 0
        self._seat = set()
        self._occupied = set()
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for y, line in enumerate(input):
                for x, col in enumerate(line.rstrip()):
                    if col == "L":
                        self._seat.add((y, x))
                    self._x_max = x + 1
                self._y_max = y + 1
        # First round, all seat become occupied.
        self._occupied = self._seat.copy()
        # Second round, release occupied seat.
        to_release = set()
        to_take = set()
        while True:
            for seat in self._seat:
                if self.is_occupied(*seat) and self.nb_adjacent_seat_occupied(*seat) >= 4:
                    to_release.add(seat)
            if len(to_release) != 0:
                for seat in to_release:
                    self._occupied.remove(seat)
                to_release.clear()
            else:
                break
            for seat in self._seat:
                if not self.is_occupied(*seat) and self.nb_adjacent_seat_occupied(*seat) == 0:
                    to_take.add(seat)
            if len(to_take) != 0:
                for seat in to_take:
                    self._occupied.add(seat)
                to_take.clear()
        print(f"Part 1: {len(self._occupied)}")

    def is_seat(self, y: int, x: int) -> bool:
        return (y, x) in self._seat

    def is_occupied(self, y: int, x: int) -> bool:
        return (y, x) in self._occupied

    def nb_adjacent_seat_occupied(self, y: int, x: int) -> int:
        test = set([
            (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
            (y, x - 1), (y, x + 1),
            (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)
        ])
        count = 0
        for pos in test:
            if self.is_occupied(*pos):
                count += 1
        return count

    def print(self):
        s = ""
        for y in range(self._y_max):
            for x in range(self._x_max):
                if self.is_seat(y, x):
                    if self.is_occupied(y, x):
                        s += "#"
                    else:
                        s += "L"
                else:
                    s += "."
            s += "\n"
        print(s)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day11(args.input)
