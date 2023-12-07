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


def get_rank(cards: Dict[str, int], joker: bool) -> HandLevel:
    nb_type = len(cards)
    figures = list(cards)
    values = cards.values()
    level: HandLevel
    # Only one element: only a five kind.
    if nb_type == 1:
        level = HandLevel.K5
    # Two elements => multi combinaison to check [1+4, 2+3].
    elif nb_type == 2:
        # Joker: five kind [1J+4, 1+4J, 2J+3, 2+3J].
        if joker and 'J' in figures:
            level = HandLevel.K5
        # One type as four cards (4 + 1): four kind.
        elif 4 in values:
            level = HandLevel.K4
        # Remaining full house (3 + 2).
        else:
            level = HandLevel.FH
    # Three elements: multi combinaison to check [1+1+3, 1+2+2].
    elif nb_type == 3:
        # Joker: four kind or full house
        # [1+(1J+3), 1+(1+3J), 1+(2+2J), !! (1J+2)+2 !!].
        if joker and 'J' in figures:
            if cards['J'] == 1 and 3 not in values:
                level = HandLevel.FH
            else:
                level = HandLevel.K4
        # One type as three cards: three kind.
        elif 3 in values:
            level = HandLevel.K3
        # Remaining a double pair.
        else:
            level = HandLevel.P2
    # Three elements: only a simple pair [1+1+1+2].
    elif nb_type == 4:
        # Joker: three kind [1+1+(1J+2), 1+1+(1+2J)].
        if joker and 'J' in figures:
            level = HandLevel.K3
        else:
            level = HandLevel.P1
    # Joker: one pair [1+1+1+(1+1J)].
    elif joker and 'J' in figures:
        level = HandLevel.P1
    # Five elements: high cards [1+1+1+1+1].
    else:
        level = HandLevel.HI
    return level


def parse(puzzle_in: List[str], joker: bool) -> List[Hand]:
    hands: List[Hand] = []
    for line in puzzle_in:
        cards, bid = line.split()
        cards_count = Counter(cards)
        hands.append((cards, get_rank(cards_count, joker), int(bid)))
    return hands


def order_hands(hands: List[Hand], joker: bool) -> List[Hand]:
    hand_order: List[str]
    if joker:
        hand_order = [
            'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'
        ]
    else:
        hand_order = [
            'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'
        ]
    hands.sort(key=lambda o: [hand_order.index(c) for c in o[0]], reverse=True)
    hands.sort(key=lambda c: c[1])
    return hands


def get_score(hands: List[Hand]) -> int:
    score = 0
    rank = 1
    for _, _, bid in hands:
        score += bid * rank
        rank += 1
    return score


def process(puzzle_in: List[str]):
    print(f"Part 1: {get_score(order_hands(parse(puzzle_in, False), False))}")
    print(f"Part 2: {get_score(order_hands(parse(puzzle_in, True), True))}")
