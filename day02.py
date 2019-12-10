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
        # Day 2.1: 1202 progrma alarm.
        day2_1 = self.intcode_execute(data, 12, 2)
        print(f"Day2.1: {day2_1}")
        # Day 2.2: Search parameter for output 19690720.
        for noun in range(0, 99):
            for verb in range(0,99):
                if self.intcode_execute(data, noun, verb) == 19690720:
                    print(f"Day2.2: {100 * noun + verb}")

    def intcode_execute(self, memory, noun, verb):
        # Copy memory for running program.
        runtime = memory.copy()
        # Set noun and verb parameter.
        runtime[1] = noun
        runtime[2] = verb
        # Execute program.
        i = 0
        while i < len(runtime):
            opcode = runtime[i]
            # Add instruction.
            if opcode == 1:
                # Get arguments.
                arg1 = runtime[i+1]
                arg2 = runtime[i+2]
                out = runtime[i+3]
                # Move to next opcode.
                i += 4
                # Add arguments, and set value to out position.
                runtime[out] = runtime[arg1] + runtime[arg2]
            # Multiply instruction.
            elif opcode == 2:
                # Get arguments.
                arg1 = runtime[i+1]
                arg2 = runtime[i+2]
                out = runtime[i+3]
                # Move to next opcode.
                i += 4
                # Multiply arguments, and set value to out position.
                runtime[out] = runtime[arg1] * runtime[arg2]
            # Halt instruction.
            elif opcode == 99:
                break
        # Return program output.
        return runtime[0]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 2 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day2(args.input)
