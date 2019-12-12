#! /usr/bin/env python3
import argparse
import re


class Day12:
    """ Day 12: The N-Body Problem """
    def __init__(self, input_file):
        self.moons = []
        self.velocities = []
        self.steps = 1000
        self.process(input_file)

    def process(self, input_file):
        # Read input data.
        with open(input_file, "r") as input:
            for moon in input:
                self.moons.append([int(s) for s in re.findall(r'-?\d+', moon)])
                self.velocities.append([0,0,0])
        # Simulate all system interaction.
        for _ in range(self.steps):
            for i in range(len(self.moons)):
                self.update_moon_velocity(i)
            for i in range(len(self.moons)):
                self.update_moon_position(i)
        # Get total energy of the system.
        total_energy = sum(
            self.get_moon_energy(i) for i in range(len(self.moons)))
        print(f"Total system energy: {total_energy}")

    def update_moon_velocity(self, id):
        moon = self.moons[id]
        # Parse all moons of the system.
        for i in range(len(self.moons)):
            moon_cmp = self.moons[i]
            # Ignoring current moon.
            if i != id:
                # Update each velocity axis.
                for i in range(3):
                    if moon[i] < moon_cmp[i]:
                        self.velocities[id][i] += 1
                    elif moon[i] > moon_cmp[i]:
                        self.velocities[id][i] -= 1

    def update_moon_position(self, id):
        # Update each axis.
        for i in range(3):
            self.moons[id][i] += self.velocities[id][i]

    def get_moon_energy(self, id):
        pot = sum(abs(i) for i in self.moons[id])
        kin = sum(abs(i) for i in self.velocities[id])
        return pot * kin


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 12 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day12(args.input)
