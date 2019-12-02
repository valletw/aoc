#! /usr/bin/env python3
import argparse
import math


class Day1:
    """ Day 1: The Tyranny of the Rocket Equation """
    """ Fuel required to launch a given module is based on its mass.
    Specifically, to find the fuel required for a module, take its mass, divide
    by three, round down, and subtract 2. """
    """ Part 2: add fuel requirement for fuel mass until no more required. """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        total_fuel = 0
        with open(input_file, "r") as input:
            for mass in input:
                fuel = self.get_fuel(int(mass))
                total_fuel += fuel
                # Get amont of fuel for fuel required mass.
                while fuel > 0:
                    fuel = self.get_fuel(fuel)
                    # If negative fuel, no mass added.
                    if fuel > 0:
                        total_fuel += fuel
        print (f"Total fuel requirement: {total_fuel}")

    def get_fuel(self, mass):
        return math.floor(mass / 3) - 2


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 1 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day1(args.input)
