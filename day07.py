#! /usr/bin/env python3
import argparse
import array
import itertools


class Day7:
    """ Day 7: Amplification Circuit """
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
        # Parse each combinations.
        max_thruster = 0
        for settings in itertools.permutations(range(5), 5):
            signal = 0
            # Execute program.
            for phase in settings:
                signal = self.intcode_execute(data, phase, signal)
            # Check if maximum is reached.
            if max_thruster < signal:
                max_thruster = signal
        print(f"Max: {max_thruster}")

    def intcode_execute(self, memory, phase, signal):
        # Copy memory for running program.
        runtime = memory.copy()
        # Execute program.
        i = 0
        cmd = ""
        input = 0
        output = 0
        while i < len(runtime):
            opcode = int(runtime[i] % 100)
            mode = [int(m) for m in str(int(runtime[i] / 100))]
            mode.reverse()
            if len(mode) < 3:
                mode.extend([0] * (3 - len(mode)))
            # Add instruction.
            if opcode == 1:
                args, vals = self.read_params(runtime, i, mode, 3)
                # Add arguments, and set value to out position.
                cmd = f"{i}: [{args[2]}] = {vals[0]} + {vals[1]}"
                runtime[args[2]] = vals[0] + vals[1]
                # Move to next opcode.
                i += 4
            # Multiply instruction.
            elif opcode == 2:
                args, vals = self.read_params(runtime, i, mode, 3)
                # Multiply arguments, and set value to out position.
                cmd = f"{i}: [{args[2]}] = {vals[0]} * {vals[1]}"
                runtime[args[2]] = vals[0] * vals[1]
                # Move to next opcode.
                i += 4
            # Stdin instruction
            elif opcode == 3:
                args, vals = self.read_params(runtime, i, mode, 1)
                # Read input.
                if input == 0:
                    cmd = f"{i}: [{args[0]}] = {phase} (phase)"
                    runtime[args[0]] = phase
                    input += 1
                else:
                    cmd = f"{i}: [{args[0]}] = {signal} (signal)"
                    runtime[args[0]] = signal
                # Move to next opcode
                i += 2
            # Stdout instruction
            elif opcode == 4:
                args, vals = self.read_params(runtime, i, mode, 1)
                # Write output.
                cmd = f"{i}: output = [{args[0]}]"
                output = runtime[args[0]]
                # Move to next opcode
                i += 2
            # Branch if true instruction.
            elif opcode == 5:
                args, vals = self.read_params(runtime, i, mode, 2)
                cmd = f"{i}: cbnz {vals[0]}, {vals[1]}"
                if vals[0] != 0:
                    i = vals[1]
                else:
                    # Move to next opcode
                    i += 3
            # Branch if false instruction.
            elif opcode == 6:
                args, vals = self.read_params(runtime, i, mode, 2)
                cmd = f"{i}: cbz {vals[0]}, {vals[1]}"
                if vals[0] == 0:
                    i = vals[1]
                else:
                    # Move to next opcode
                    i += 3
            # Less than instruction.
            elif opcode == 7:
                args, vals = self.read_params(runtime, i, mode, 3)
                cmd = f"{i}: [{args[2]}] = {vals[0]} < {vals[1]}"
                if vals[0] < vals[1]:
                    runtime[args[2]] = 1
                else:
                    runtime[args[2]] = 0
                # Move to next opcode
                i += 4
            # Equal instruction.
            elif opcode == 8:
                args, vals = self.read_params(runtime, i, mode, 3)
                cmd = f"{i}: [{args[2]}] = {vals[0]} == {vals[1]}"
                if vals[0] == vals[1]:
                    runtime[args[2]] = 1
                else:
                    runtime[args[2]] = 0
                # Move to next opcode
                i += 4
            # Halt instruction.
            elif opcode == 99:
                cmd = f"{i}: halt"
                break
        # Return program output.
        return output

    def read_params(self, memory, idx, mode, nb):
        # Get arguments.
        args = []
        for j in range(1, nb + 1):
            args.append(memory[idx + j])
        # Check for mode.
        vals = []
        for j in range(0, nb):
            if mode[j] == 0:
                vals.append(memory[args[j]])
            else:
                vals.append(args[j])
        return args, vals


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 7 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day7(args.input)
