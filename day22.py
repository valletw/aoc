#! /usr/bin/env python3
import argparse


class Day22:
    """ Day 22: Slam Shuffle """
    def __init__(self, input_file):
        self.deck1 = DeckMin(10007, 2019)
        self.deck2 = DeckMin(119315717514047, 2020)
        self.deck2_card = 2020
        self.deck2_repeat = 101741582076661
        self.process(input_file)

    def process(self, input_file):
        inst = []
        with open(input_file, "r") as input:
            for line in input:
                inst.append(line.rstrip())
        self.inst_exec(inst, self.deck1)
        card = self.deck1.get_position()
        print(f"Part1: card 2019 @{card}")
        # Find cycle.
        cycle = 0
        for i in range(self.deck2_repeat):
            self.inst_exec(inst, self.deck2)
            if self.deck2.get_position() == self.deck2_card:
                cycle = i
                break
        # Execute the last cycle only.
        r = self.deck2_repeat % cycle
        for _ in range(r):
            self.inst_exec(inst, self.deck2)
        card = self.deck2.get_position()
        print(f"Part2: card 2020 @{card} {cycle}")

    def inst_exec(self, inst, deck):
        for line in inst:
            if deck.method_cmp(line, "deal_new"):
                deck.deal_new()
            elif deck.method_cmp(line, "deal_inc"):
                n = deck.method_get_int(line, "deal_inc")
                deck.deal_increment(n)
            elif deck.method_cmp(line, "cut"):
                n = deck.method_get_int(line, "cut")
                deck.cut(n)


class DeckMin:
    def __init__(self, size: int, follow: int):
        self.deck = size
        self.card = follow
        self.methods = {
            'deal_new': "deal into new stack",
            'deal_inc': "deal with increment",
            'cut': "cut"
        }

    def check(self):
        assert self.card >= 0
        assert self.card < self.deck

    def method_cmp(self, str, method):
        return str[:len(self.methods[method])] == self.methods[method]

    def method_get_int(self, str, method):
        return int(str[len(self.methods[method]):])

    def deal_new(self):
        # Reverse deck.
        self.card = self.deck - self.card - 1
        self.check()

    def deal_increment(self, inc: int):
        self.card *= inc
        self.card %= self.deck
        self.check()

    def cut(self, n: int):
        # Get cut position
        if n < 0:
            p = self.deck + n
        else:
            p = n
        if self.card < p:
            # Card position at/before cut position (go to bottom).
            self.card += self.deck - p
        else:
            # Card position after cut position (return on top).
            self.card -= p
        self.check()

    def get_position(self):
        return self.card


class Deck:
    def __init__(self, size: int, debug=False):
        self.deck = [i for i in range(size)]
        self.methods = {
            'deal_new': "deal into new stack",
            'deal_inc': "deal with increment",
            'cut': "cut"
        }
        self.debug = debug

    def method_cmp(self, str, method):
        return str[:len(self.methods[method])] == self.methods[method]

    def method_get_int(self, str, method):
        return int(str[len(self.methods[method]):])

    def deal_new(self):
        if self.debug:
            print(f"{self.methods['deal_new']}")
        self.deck.reverse()
        if self.debug:
            print(self.deck)

    def deal_increment(self, inc: int):
        if self.debug:
            print(f"{self.methods['deal_inc']} {inc}")
        new_deck = [0] * len(self.deck)
        i = 0
        run = 0
        for c in self.deck:
            new_deck[i] = c
            i += inc
            if i >= len(self.deck):
                run += 1
                i -= len(self.deck)
                if i == inc:
                    i -= run
                elif i == 0:
                    i = inc - run
        self.deck = new_deck
        if self.debug:
            print(self.deck)

    def cut(self, n: int):
        if self.debug:
            print(f"{self.methods['cut']} {n}")
        if n < 0:
            n = len(self.deck) + n
        tmp = self.deck[0:n]
        self.deck = self.deck[n:]
        self.deck.extend(tmp)
        if self.debug:
            print(self.deck)

    def get_card_position(self, card):
        return self.deck.index(card)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 22 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day22(args.input)
