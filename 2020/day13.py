#!/usr/bin/env python3
import argparse
import math


class Day13:
    """ Day 13: Shuttle Search """

    def __init__(self, input_file):
        self._time_departure = 0
        self._bus_line = list()
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                data.append(line.rstrip())
        self._time_departure = int(data[0])
        for idx, bus in enumerate(data[1].split(",")):
            if bus != "x":
                self._bus_line.append((int(bus), idx))
        next_departure = set()
        for bus in self._bus_line:
            it = math.ceil(self._time_departure / bus[0])
            next_departure.add((it * bus[0], bus[0]))
        next_departure = sorted(next_departure)
        time_wait = next_departure[0][0] - self._time_departure
        print(f"Part 1: {time_wait * next_departure[0][1]}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day13(args.input)
