#! /usr/bin/env python3
import argparse
import math


class Day10:
    """ Day 10: Monitoring Station """
    def __init__(self, input_file):
        self.x_max = 0
        self.y_max = 0
        self.grid = []
        self.asteroids = []
        self.process(input_file)

    def process(self, input_file):
        # Read input data, and convert to boolean matrix.
        with open(input_file, "r") as input:
            for line in input:
                self.x_max = max(len(line) - 1, self.x_max)
                self.y_max += 1
                self.grid.append([True if a == '#' else False
                    for a in line.rstrip()])
        # Find all asteroids.
        for y in range(0, self.y_max):
            for x in range(0, self.x_max):
                if self.grid[y][x]:
                    self.asteroids.append((x, y))
        # Get number of detected asteroids from each posible stations.
        stations_data = []
        for station in self.asteroids:
            detected = set()
            for asteroid in self.asteroids:
                if station != asteroid:
                    dx = asteroid[0] - station[0]
                    dy = asteroid[1] - station[1]
                    g = abs(math.gcd(dx, dy))
                    detected.add((dx // g, dy // g))
            stations_data.append((len(detected), station, detected))
        stations_data.sort(reverse=True)
        max_detected, _, _ = stations_data[0]
        print(f"Best location: {max_detected}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 10 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day10(args.input)
