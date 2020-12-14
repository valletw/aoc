#!/usr/bin/env python3
import argparse


class Day14:
    """ Day 14: Docking Data """

    def __init__(self, input_file):
        self._mask_and = 0xfffffffff
        self._mask_or = 0
        self._memory = dict()
        self.process(input_file)

    def process(self, input_file):
        data = list()
        with open(input_file, "r") as input:
            for line in input:
                data.append(line.rstrip())
        for d in data:
            action, value = d.split(" = ")
            if action == "mask":
                for idx, bit in enumerate(value):
                    idx = 35 - idx
                    if bit == "X":
                        self._mask_and |= 1 << idx
                        self._mask_or &= ~(1 << idx)
                    elif bit == "1":
                        self._mask_and |= 1 << idx
                        self._mask_or |= 1 << idx
                    elif bit == "0":
                        self._mask_and &= ~(1 << idx)
                        self._mask_or &= ~(1 << idx)
            else:
                mem_id = int(action.replace("]", "").split("[")[1])
                val = int(value)
                self._memory[mem_id] = (val | self._mask_or) & self._mask_and
        mem_sum = sum([val for _, (_, val) in enumerate(self._memory.items())])
        print(f"Part 1: {mem_sum}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day14(args.input)
