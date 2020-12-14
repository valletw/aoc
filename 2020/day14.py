#!/usr/bin/env python3
import argparse


class Day14:
    """ Day 14: Docking Data """

    def __init__(self, input_file):
        self._mask_and = 0xfffffffff
        self._mask_or = 0
        self._mask_float = 0
        self._memory_1 = dict()
        self._memory_2 = dict()
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
                        self._mask_float |= 1 << idx
                    elif bit == "1":
                        self._mask_and |= 1 << idx
                        self._mask_or |= 1 << idx
                        self._mask_float &= ~(1 << idx)
                    elif bit == "0":
                        self._mask_and &= ~(1 << idx)
                        self._mask_or &= ~(1 << idx)
                        self._mask_float &= ~(1 << idx)
            else:
                mem_id = int(action.replace("]", "").split("[")[1])
                mem_ids = list()
                val = int(value)
                self._memory_1[mem_id] = (val | self._mask_or) & self._mask_and
                mem_ids.append((mem_id | self._mask_and) & ~self._mask_float)
                for idx in range(36):
                    if self._mask_float & (1 << idx):
                        mem_ids.extend(mem_ids.copy())
                        it_start = int(len(mem_ids) / 2)
                        for i, v in enumerate(mem_ids[it_start:]):
                            mem_ids[it_start + i] = v | (1 << idx)
                mem_ids = list(dict.fromkeys(mem_ids))
                for idx in mem_ids:
                    self._memory_2[idx] = val
        mem_sum_1 = sum([val for _, (_, val) in enumerate(self._memory_1.items())])
        mem_sum_2 = sum([val for _, (_, val) in enumerate(self._memory_2.items())])
        print(f"Part 1: {mem_sum_1}")
        print(f"Part 2: {mem_sum_2}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day14(args.input)
