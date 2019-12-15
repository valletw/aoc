#! /usr/bin/env python3
import argparse
import math


class Day14:
    """ Day 14: Space Stoichiometry """
    def __init__(self, input_file):
        self.reactions = dict()
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            for line in input:
                line = line.rstrip()
                reacts_form, prod = line.split(' => ')
                reacts = reacts_form.split(', ')
                react_list = list()
                for react in reacts:
                    r = react.split(' ')
                    react_list.append((r[1], int(r[0])))
                p = prod.split(' ')
                self.reactions[(p[1], int(p[0]))] = react_list
        _, fuel_reactifs = self.find_reactifs('FUEL')
        while len(fuel_reactifs) != 1:
            fuel_reactifs = self.reduce_formula(fuel_reactifs)
        print(f"1 FUEL = {fuel_reactifs[0][1]} {fuel_reactifs[0][0]}")

    def find_reactifs(self, name):
        reactifs = list()
        nb_producted = 0
        for key, val in self.reactions.items():
            if name == key[0]:
                reactifs = val
                nb_producted = key[1]
                break
        return nb_producted, reactifs

    def reduce_formula(self, formula):
        reduc = list()
        leftover = list()
        # Parse all reactifs and find how to produce them.
        for reactif in formula:
            name, nb = reactif
            if nb <= 0:
                continue
            if name != 'ORE':
                nb_producted, reactifs = self.find_reactifs(name)
                # Calculate the ratio in order to have enough production.
                ratio = math.ceil(nb / nb_producted)
                # Get excess production.
                over_prod = (nb_producted * ratio) - nb
                if over_prod != 0:
                    leftover.append((name, over_prod))
                # Update reactifs list with new ratio to reduce list.
                for r in reactifs:
                    reduc.append((r[0], r[1] * ratio))
            else:
                reduc.append(reactif)
        # Reorder the reduced formula and aggregate reactifs.
        reduc.sort()
        leftover.sort()
        reduc_aggr = [reduc[0]]
        for i in range(1, len(reduc)):
            if reduc[i][0] == reduc[i-1][0]:
                last = reduc_aggr.pop()
                reduc_aggr.append((last[0], last[1] + reduc[i][1]))
            else:
                reduc_aggr.append(reduc[i])
        # Remove over production.
        for i in range(len(reduc_aggr)):
            for name, nb in leftover:
                if name == reduc_aggr[i][0]:
                    # Remove excess production.
                    nb = reduc_aggr[i][1] - nb
                    if nb < 0:
                        nb = 0
                    reduc_aggr[i] = (name, nb)
        return reduc_aggr


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 14 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day14(args.input)
