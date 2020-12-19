#!/usr/bin/env python3
import argparse


class Day18:
    """ Day 18: Operation Order """

    def __init__(self, input_file):
        self.process(input_file)

    def process(self, input_file):
        expression = str()
        with open(input_file, "r") as input:
            for line in input:
                expression = line.rstrip()
        new_exp = expression.copy()
        while True:
            par_open = new_exp.find("(")
            result = self.compute_expression(new_exp[:par_open - 1])

        result = self.find_expression(expression)
        print(f"Part 1: {result}")

    def find_expression(self, exp: str) -> int:
        result = 0
        par_open = exp.find("(")
        par_close = exp.find(")")
        if par_open != -1:
            par_open_n = exp[par_open + 1:].find("(")
            result = self.find_expression(exp[par_open + 1:])
        elif par_close != -1:
            result = self.compute_expression(exp[:par_close - 1])
        else:
            result = self.compute_expression(exp)
        return result

    def compute_expression(self, exp: str) -> int:
        data = exp.split(" ")
        op = "+"
        result = 0
        for d in data:
            if d in ["+", "-", "*", "/"]:
                op = d
            else:
                result = eval(str(result) + op + d)
        return result


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day18(args.input)
