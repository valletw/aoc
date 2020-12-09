#!/usr/bin/env python3
import argparse


class Day9:
    """ Day 9: Encoding Error """
    _PREAMBLE_SIZE = 25

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                data.append(int(line))
        invalid_number = 0
        for num_id, num in enumerate(data[self._PREAMBLE_SIZE:]):
            found = False
            # Get N numbers previous the current number.
            preamble = data[num_id:self._PREAMBLE_SIZE + num_id]
            for p1_id, p1 in enumerate(preamble):
                for p2 in preamble[p1_id + 1:]:
                    if p1 + p2 == num:
                        found = True
                        break
                if found:
                    break
            if not found:
                invalid_number = num
                break
        print(f"Part 1: {invalid_number}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day9(args.input)
