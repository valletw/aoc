#!/usr/bin/env python3
import argparse
import math
from enum import Enum


class BoatDirection(Enum):
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    NORTH = (0, 1)


class Boat:
    def __init__(self):
        self._position = (0, 0)
        self._direction = BoatDirection.EAST

    def move(self, direction: BoatDirection, unit: int):
        x, y = self._position
        x += direction.value[0] * unit
        y += direction.value[1] * unit
        self._position = (x, y)

    def forward(self, unit: int):
        self.move(self._direction, unit)

    def turn(self, left: bool, angle: int):
        directions = [
            BoatDirection.EAST,
            BoatDirection.SOUTH,
            BoatDirection.WEST,
            BoatDirection.NORTH
        ]
        dir_inc = math.floor(angle / 90)
        if left:
            dir_inc = -dir_inc
        dir_id = directions.index(self._direction) + dir_inc
        dir_id %= len(directions)
        self._direction = directions[dir_id]

    def get_distance(self) -> int:
        return abs(self._position[0]) + abs(self._position[1])


class Day12:
    """ Day 12: Rain Risk """

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                line = line.rstrip()
                data.append((line[0], int(line[1:])))
        boat = Boat()
        for inst in data:
            action, unit = inst
            if action == "N":
                boat.move(BoatDirection.NORTH, unit)
            elif action == "S":
                boat.move(BoatDirection.SOUTH, unit)
            elif action == "E":
                boat.move(BoatDirection.EAST, unit)
            elif action == "W":
                boat.move(BoatDirection.WEST, unit)
            elif action == "L":
                boat.turn(True, unit)
            elif action == "R":
                boat.turn(False, unit)
            elif action == "F":
                boat.forward(unit)
        print(f"Part 1: {boat.get_distance()}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day12(args.input)
