#!/usr/bin/env python3
import argparse
import math
from enum import Enum


class BoatDirection(Enum):
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    NORTH = (0, 1)


class Boat1:
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


class Boat2:
    def __init__(self, waypoint):
        self._position = (0, 0)
        self._waypoint = waypoint

    def move(self, direction: BoatDirection, unit: int):
        x, y = self._waypoint
        x += direction.value[0] * unit
        y += direction.value[1] * unit
        self._waypoint = (x, y)

    def forward(self, unit: int):
        x, y = self._position
        x += self._waypoint[0] * unit
        y += self._waypoint[1] * unit
        self._position = (x, y)

    def turn(self, left: bool, angle: int):
        dir_inc = math.floor(angle / 90) % 4
        x, y = self._waypoint
        if dir_inc == 2:
            x = -x
            y = -y
        elif dir_inc == 1:
            if (0 <= x and 0 <= y) \
                or (x <= 0 and y <= 0):
                if left:
                    x = -x
                else:
                    y = -y
            elif (x <= 0 and 0 <= y) \
                or (0 <= x and y <= 0):
                if left:
                    y = -y
                else:
                    x = -x
        elif dir_inc == 3:
            if (0 <= x and 0 <= y) \
                or (x <= 0 and y <= 0):
                if not left:
                    x = -x
                else:
                    y = -y
            elif (x <= 0 and 0 <= y) \
                or (0 <= x and y <= 0):
                if not left:
                    y = -y
                else:
                    x = -x
        self._waypoint = (x ,y)

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
        boat1 = Boat1()
        boat2 = Boat2((10, 1))
        for inst in data:
            action, unit = inst
            if action == "N":
                boat1.move(BoatDirection.NORTH, unit)
                boat2.move(BoatDirection.NORTH, unit)
            elif action == "S":
                boat1.move(BoatDirection.SOUTH, unit)
                boat2.move(BoatDirection.SOUTH, unit)
            elif action == "E":
                boat1.move(BoatDirection.EAST, unit)
                boat2.move(BoatDirection.EAST, unit)
            elif action == "W":
                boat1.move(BoatDirection.WEST, unit)
                boat2.move(BoatDirection.WEST, unit)
            elif action == "L":
                boat1.turn(True, unit)
                boat2.turn(True, unit)
            elif action == "R":
                boat1.turn(False, unit)
                boat2.turn(False, unit)
            elif action == "F":
                boat1.forward(unit)
                boat2.forward(unit)
        print(f"Part 1: {boat1.get_distance()}")
        print(f"Part 2: {boat2.get_distance()}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day12(args.input)
