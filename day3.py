#! /usr/bin/env python3
import argparse
import math


class Day3:
    """ Day 3: Crossed Wires """

    def __init__(self, input_file):
        self.grid_len = 40000
        self.grid = [[0] * self.grid_len for i in range(self.grid_len)]
        self.process(input_file)

    def process(self, input_file):
        list = []
        # Read all input data.
        with open(input_file, "r") as input:
            for line in input:
                list.append(line.split(","))
        # Parse wires list and fill grid, check distance at same time.
        distance = self.grid_len
        wire_id = 0
        for wire in list:
            row = int(self.grid_len / 2)
            col = int(self.grid_len / 2)
            wire_id += 1
            for data in wire:
                direction = data[0]
                size = int(data[1:])
                for i in range(0, size):
                    if direction == "R":
                        col += 1
                    elif direction == "L":
                        col -= 1
                    elif direction == "U":
                        row -= 1
                    elif direction == "D":
                        row += 1
                    # Check if no wire on grid.
                    if self.grid[row][col] == 0:
                        self.grid[row][col] = wire_id
                    # If another wire (cross), get distance.
                    elif self.grid[row][col] != wire_id:
                        dist = math.fabs(int(self.grid_len / 2) - row) \
                            + math.fabs(int(self.grid_len / 2) - col)
                        if dist < distance:
                            distance = dist
        print(f"Distance: {int(distance)}")
        return


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 3 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day3(args.input)
