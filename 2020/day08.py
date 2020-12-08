#!/usr/bin/env python3
import argparse


class Program:
    """ Program executor """
    def __init__(self, prog: list, acc: int = 0):
        self._acc = acc
        self._prog = prog

    def get_acc(self) -> int:
        return self._acc

    def process(self):
        executed = [False for _ in range(len(self._prog))]
        pc = 0
        while True:
            if executed[pc]:
                break
            executed[pc] = True
            op, arg = self._prog[pc].split(" ")
            if op == "acc":
                # Accumulator.
                self._acc += int(arg)
                pc += 1
            elif op == "jmp":
                # Jumps.
                pc += int(arg)
            else:
                # No operation.
                pc += 1


class Day8:
    """ Day 8: Handheld Halting """
    def __init__(self, input_file):
        self._instructions = list()
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            for line in input:
                self._instructions.append(line.rstrip())
        prog = Program(self._instructions)
        prog.process()
        print(f"Part 1: {prog.get_acc()}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day8(args.input)
