from typing import List, Tuple


# (WIN, NUM)
Card = Tuple[List[int], List[int]]


def parse_card(puzzle_in: List[str]) -> List[Card]:
    cards: List[Card] = []
    for line in puzzle_in:
        # Extract winning numbers and numbers from each card.
        lists = line.split(":")[1].strip()
        win_s, num_s = lists.split("|")
        # Convert strings to integer list (avoid double space).
        win = [int(n) for n in win_s.strip().replace("  ", " ").split(" ")]
        num = [int(n) for n in num_s.strip().replace("  ", " ").split(" ")]
        # Add card to the list.
        cards.append((win, num))
    return cards


def compute_points(cards: List[Card]) -> List[int]:
    points: List[int] = []
    for winning, numbers in cards:
        # Count matching number between the two lists.
        counts = sum(i in numbers for i in winning)
        # Compute points.
        points.append(pow(2, counts - 1) if counts != 0 else 0)
    return points


def process(puzzle_in: List[str]):
    cards = parse_card(puzzle_in)
    print(f"Part 1: {sum(compute_points(cards))}")
