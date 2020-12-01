#! /usr/bin/env python3
import argparse
import math
import re


class Day12:
    """ Day 12: The N-Body Problem """
    def __init__(self, input_file):
        self.moons_init = []
        self.moons = []
        self.velocities_init = []
        self.velocities = []
        self.steps = 1000
        self.process(input_file)

    def process(self, input_file):
        # Read input data.
        with open(input_file, "r") as input:
            for moon in input:
                self.moons_init.append(
                    [int(s) for s in re.findall(r'-?\d+', moon)])
                self.velocities_init.append([0,0,0])
        # Simulate all system interaction.
        self.moons = self.moons_init.copy()
        self.velocities = self.velocities_init.copy()
        for _ in range(self.steps):
            for i in range(len(self.moons)):
                self.update_moon_velocity(i)
            for i in range(len(self.moons)):
                self.update_moon_position(i)
        # Get total energy of the system.
        total_energy = sum(
            self.get_moon_energy(i) for i in range(len(self.moons)))
        print(f"Total system energy: {total_energy}")
        # Find system cycle.
        self.moons = self.moons_init.copy()
        self.velocities = self.velocities_init.copy()
        axis = [set(), set(), set()]
        add_axis = [True,True,True]
        while add_axis != [False,False,False]:
            # Get all axis values.
            a = [tuple((self.moons[j][i], self.velocities[j][i])
                    for j in range(len(self.moons)))
                for i in range(3)]
            # Check if axis already exist.
            for i in range(3):
                if add_axis[i] and a[i] not in axis[i]:
                    axis[i].add(a[i])
                else:
                    add_axis[i] = False
            # Do step.
            for i in range(len(self.moons)):
                self.update_moon_velocity(i)
            for i in range(len(self.moons)):
                self.update_moon_position(i)
        print(f"Cycle found: {lcm_list([len(a) for a in axis])} steps")

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


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm_list(data):
    if len(data) == 2:
        return lcm(data[0], data[1])
    else:
        return lcm(data[0], lcm_list(data[1:]))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 12 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day12(args.input)
