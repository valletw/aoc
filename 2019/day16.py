#! /usr/bin/env python3
import argparse


class Day16:
    """ Day 16: Flawed Frequency Transmission """
    def __init__(self, input_file):
        self.nb_phase = 100
        self.pattern = [0, 1, 0, -1]
        self.process(input_file)

    def process(self, input_file):
        signal = []
        with open(input_file, "r") as input:
            line = input.read().rstrip()
            for d in line:
                signal.append(int(d))
        for _ in range(self.nb_phase):
            signal = self.fft(signal)
        print(f"Final output 8-digits: {''.join(str(i) for i in signal[:8])}")

    def fft(self, signal):
        output = []
        size = len(signal)
        for i in range(size):
            pattern = self.generate_pattern(i + 1, size)
            tmp = []
            for d, p in zip(signal, pattern):
                tmp.append(d * p)
            output.append(abs(sum(tmp)) % 10)
        return output

    def generate_pattern(self, nb, size):
        pattern = [p for p in self.pattern for i in range(nb)]
        while len(pattern) < size + 1:
            pattern.extend(pattern)
        return pattern[1:size + 1]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 16 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day16(args.input)
