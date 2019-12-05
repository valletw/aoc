#! /usr/bin/env python3
import argparse
import array


class Day5:
    """ Day 5: Sunny with a Chance of Asteroids """
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
        # Execute program.
        self.intcode_execute(data)

    def intcode_execute(self, memory):
        # Copy memory for running program.
        runtime = memory.copy()
        # Execute program.
        i = 0
        cmd = ""
        while i < len(runtime):
            opcode = int(runtime[i] % 100)
            mode = [int(m) for m in str(int(runtime[i] / 100))]
            mode.reverse()
            if len(mode) < 3:
                mode.extend([0] * (3 - len(mode)))
            # Add instruction.
            if opcode == 1:
                # Get arguments.
                args = []
                for j in range(1, 4):
                    args.append(runtime[i + j])
                # Check for mode.
                vals = []
                for j in range(0, 3):
                    if mode[j] == 0:
                        vals.append(runtime[args[j]])
                    else:
                        vals.append(args[j])
                # Add arguments, and set value to out position.
                cmd = f"{i}: [{args[2]}] = {vals[0]} + {vals[1]}"
                runtime[args[2]] = vals[0] + vals[1]
                # Move to next opcode.
                i += 4
            # Multiply instruction.
            elif opcode == 2:
                # Get arguments.
                args = []
                for j in range(1, 4):
                    args.append(runtime[i + j])
                # Check for mode.
                vals = []
                for j in range(0, 3):
                    if mode[j] == 0:
                        vals.append(runtime[args[j]])
                    else:
                        vals.append(args[j])
                # Multiply arguments, and set value to out position.
                cmd = f"{i}: [{args[2]}] = {vals[0]} * {vals[1]}"
                runtime[args[2]] = vals[0] * vals[1]
                # Move to next opcode.
                i += 4
            # Stdin instruction
            elif opcode == 3:
                # Get arguments.
                out = runtime[i + 1]
                # Read input.
                runtime[out] = int(input(f"$ "))
                # Move to next opcode
                i += 2
            # Stdout instruction
            elif opcode == 4:
                # Get arguments.
                out = runtime[i + 1]
                # Write output.
                print(f"> {runtime[out]}")
                if runtime[out] != 0:
                    print(cmd)
                # Move to next opcode
                i += 2
            # Halt instruction.
            elif opcode == 99:
                break
        # Return program output.
        return runtime[0]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 5 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day5(args.input)
