from enum import IntEnum
from typing import List, Tuple, Dict
from collections import Counter


class HandLevel(IntEnum):
    HI = 0  # High card: distinct labels.
    P1 = 1  # One pair.
    P2 = 2  # Double pair.
    K3 = 3  # Three kind.
    FH = 4  # Full house.
    K4 = 5  # Four kind.
    K5 = 6  # Five kind.


# (CARDS, RANK, BID)
Hand = Tuple[str, HandLevel, int]


def get_rank(cards: Dict[str, int]) -> HandLevel:
    nb_type = len(cards)
    values = cards.values()
    level = HandLevel.HI
    # Only one element: only a five kind.
    if nb_type == 1:
        level = HandLevel.K5
    # Two elements => multi combinaison to check [1+4, 2+3].
    elif nb_type == 2:
        # One type as four cards (4 + 1): four kind.
        if 4 in values:
            level = HandLevel.K4
        # Remaining full house (3 + 2).
        else:
            level = HandLevel.FH
    # Three elements: multi combinaison to check [1+1+3, 1+2+2].
    elif nb_type == 3:
        # One type as three cards: three kind.
        if 3 in values:
            level = HandLevel.K3
        # Remaining a double pair.
        else:
            level = HandLevel.P2
    # Three elements: only a simple pair.
    elif nb_type == 4:
        level = HandLevel.P1
    return level


def parse(puzzle_in: List[str]) -> List[Hand]:
    hands: List[Hand] = []
    for line in puzzle_in:
        cards, bid = line.split()
        cards_count = Counter(cards)
        hands.append((cards, get_rank(cards_count), int(bid)))
    return hands


def order_hands(hands: List[Hand]) -> List[Hand]:
    hand_order = [
        'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'
    ]
    hands.sort(key=lambda o: [hand_order.index(c) for c in o[0]], reverse=True)
    hands.sort(key=lambda c: c[1])
    return hands


def process(puzzle_in: List[str]):
    hands = order_hands(parse(puzzle_in))
    p1_score = 0
    rank = 1
    for _, _, bid in hands:
        p1_score += bid * rank
        rank += 1
    print(f"Part 1: {p1_score}")
