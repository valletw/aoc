#! /usr/bin/env python3
import argparse


class Day16:
    """ Day 16: Flawed Frequency Transmission """
    def __init__(self, input_file):
        self.nb_phase = 100
        self.repeat = 10000
        self.pattern = [0, 1, 0, -1]
        self.process(input_file)

    def process(self, input_file):
        signal = []
        with open(input_file, "r") as input:
            line = input.read().rstrip()
            for d in line:
                signal.append(int(d))
        # Part 1: test FFT.
        out = self.process_signal(signal.copy())
        digits = ''.join(str(i) for i in out[:8])
        print(f"Final output 8-digits (part1): {digits}")
        # Part 2: repeat input signal.
        offset = int(''.join(str(i) for i in signal[:7]))
        out = self.process_signal(signal.copy() * self.repeat)
        digits = ''.join(str(i) for i in out[offset:offset + 8])
        print(f"Final output 8-digits (part2): {digits}")

    def process_signal(self, signal):
        for i in range(self.nb_phase):
            if i % 10 == 0:
                print('|', end=' ', flush=True)
            else:
                print('.', end=' ', flush=True)
            signal = self.fft(signal)
        print('|')
        return signal

    def fft(self, signal):
        output = []
        size = len(signal)
        for i in range(size):
            tot = 0
            mul = 1
            for ofst in range(i, size, (i + 1) * 2):
                tot += sum(signal[ofst:ofst + i + 1]) * mul
                mul *= -1
            output.append(abs(tot) % 10)
        return output


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 16 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day16(args.input)
