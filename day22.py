#! /usr/bin/env python3
import argparse


class Day22:
    """ Day 22: Slam Shuffle """
    def __init__(self, input_file, deck_size):
        self.deck = Deck(deck_size)
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            for line in input:
                if self.deck.method_cmp(line, "deal_new"):
                    self.deck.deal_new()
                elif self.deck.method_cmp(line, "deal_inc"):
                    n = self.deck.method_get_int(line, "deal_inc")
                    self.deck.deal_increment(n)
                elif self.deck.method_cmp(line, "cut"):
                    n = self.deck.method_get_int(line, "cut")
                    self.deck.cut(n)
        print(f"Card 2019 @{self.deck.get_card_position(2019)}")


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
    parser.add_argument('-s', help="Number of cards in deck",
                        default=10007, type=int, dest="deck_size")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day22(args.input, args.deck_size)
