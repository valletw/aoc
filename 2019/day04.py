#! /usr/bin/env python3
import argparse


class Day4:
    """ Day 4: Secure Container """
    """
        - It is a six-digit number.
        - The value is within the range given in your puzzle input.
        - Two adjacent digits are the same (like 22 in 122345).
        - Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
    """
    """ Part Two: the two adjacent matching digits are not part of a larger group of matching digits. """
    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        code_min = 0
        code_max = 0
        with open(input_file, "r") as input:
            s = str(input.read()).split("-")
            code_min = int(s[0])
            code_max = int(s[1])
        print(f"Combinaison: {self.get_num_combinaison(code_min, code_max)}")

    def get_num_combinaison(self, min, max):
        debug = []
        code = min
        num = 0
        while code < max:
            code += 1
            code_str = list(str(code))
            ok = False
            equal = []
            for i in range(0, len(code_str)):
                c = code_str[i]
                if i != 0:
                    if prev > c:
                        break
                    elif prev == c:
                        equal.append(int(c))
                if i == (len(code_str) - 1):
                    for e in equal:
                        if equal.count(e) == 1:
                            ok = True
                prev = c
            if ok:
                num += 1
                debug.append(code)
        print(f"{debug}")
        return num


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 4 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day4(args.input)
