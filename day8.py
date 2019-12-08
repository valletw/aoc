#! /usr/bin/env python3
import argparse
import math


class Day8:
    """ Day 8: Space Image Format """
    def __init__(self, input_file):
        self.pixel_wide = 25
        self.pixel_tall = 6
        self.process(input_file)

    def process(self, input_file):
        # Read input data.
        with open(input_file, "r") as input:
            s = input.read().rstrip()
        # Generate layers.
        layers = []
        tmp = []
        pix_id = 0
        for digit in s:
            tmp.append(int(digit))
            pix_id += 1
            if pix_id == self.pixel_wide * self.pixel_tall:
                layers.append(tmp)
                pix_id = 0
                tmp = []
        # Find layers with less 0 digit.
        min_0 = self.pixel_wide * self.pixel_tall
        layer_0 = []
        for layer in layers:
            count = layer.count(0)
            if min_0 > count:
                min_0 = count
                layer_0 = layer
        print(f"Part1: {layer_0.count(1) * layer_0.count(2)}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 8 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day8(args.input)
