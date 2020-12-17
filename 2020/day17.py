#!/usr/bin/env python3
import argparse


class Day17:
    """ Day 17: Conway Cubes """
    _CYCLES = 6

    def __init__(self, input_file):
        self._x_max = 0
        self._y_max = 0
        self._cubes_active = set()
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for y, line in enumerate(input):
                for x, cube in enumerate(line.rstrip()):
                    if cube == "#":
                        self._cubes_active.add((x, y, 0))
                    self._x_max = x + 1
                self._y_max = y + 1
        for cycle in range(self._CYCLES):
            grid = cycle + 1
            to_activate = set()
            to_inactivate = set()
            for z in range(-grid, grid + 1):
                for y in range(-grid, self._y_max + grid):
                    for x in range(-grid, self._x_max + grid):
                        pos = (x, y, z)
                        nb_active = self.nb_cube_active_nearby(*pos)
                        if self.is_active(*pos) and nb_active != 2 and nb_active != 3:
                            to_inactivate.add(pos)
                        elif not self.is_active(*pos) and nb_active == 3:
                            to_activate.add(pos)
            for cube in to_inactivate:
                self._cubes_active.remove(cube)
            for cube in to_activate:
                self._cubes_active.add(cube)
        print(f"Part 1: {len(self._cubes_active)}")

    def is_active(self, x: int, y: int, z: int) -> bool:
        return (x, y, z) in self._cubes_active

    def nb_cube_active_nearby(self, x: int, y: int, z: int) -> int:
        test = set([
            # Z-1 layer.
            (x - 1, y - 1, z - 1), (x - 1, y, z - 1), (x - 1, y + 1, z - 1),
            (x, y - 1, z - 1), (x, y, z - 1), (x, y + 1, z - 1),
            (x + 1, y - 1, z - 1), (x + 1, y, z - 1), (x + 1, y + 1, z - 1),
            # Z layer.
            (x - 1, y - 1, z), (x - 1, y, z), (x - 1, y + 1, z),
            (x, y - 1, z), (x, y + 1, z),
            (x + 1, y - 1, z), (x + 1, y, z), (x + 1, y + 1, z),
            # Z+1 layer.
            (x - 1, y - 1, z + 1), (x - 1, y, z + 1), (x - 1, y + 1, z + 1),
            (x, y - 1, z + 1), (x, y, z + 1), (x, y + 1, z + 1),
            (x + 1, y - 1, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1),
        ])
        count = 0
        for pos in test:
            if self.is_active(*pos):
                count += 1
        return count

    def print(self, cycle: int):
        grid = cycle + 1
        s = f"--- cycle={grid} ---\n"
        for z in range(-grid, grid + 1):
            s += f"*** z={z} ***\n"
            for y in range(-grid, self._y_max + grid):
                for x in range(-grid, self._x_max + grid):
                    if self.is_active(x, y, z):
                        s += "#"
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
    Day17(args.input)
