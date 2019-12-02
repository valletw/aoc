#! /usr/bin/env python3
import argparse
import array


class Day2:
    """ Day 2: 1202 Program Alarm """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        list = {}
        data = []
        # Read all input data.
        with open(input_file, "r") as input:
            list = str(input.read()).split(",")
        # Convert input data to integer array.
        for i in list:
            data.append(int(i))
        # Set 1202 program alarm state.
        data[1] = 12
        data[2] = 2
        # Execute program.
        i = 0
        while i < len(data):
            opcode = data[i]
            if opcode == 1:
                # Get arguments.
                arg1 = data[i+1]
                arg2 = data[i+2]
                out = data[i+3]
                # Move to next opcode.
                i += 4
                # Add arguments, and set value to out position.
                data[out] = data[arg1] + data[arg2]
            elif opcode == 2:
                # Get arguments.
                arg1 = data[i+1]
                arg2 = data[i+2]
                out = data[i+3]
                # Move to next opcode.
                i += 4
                # Multiply arguments, and set value to out position.
                data[out] = data[arg1] * data[arg2]
            elif opcode == 99:
                exit(f"data[0]: {data[0]}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 2 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day2(args.input)
