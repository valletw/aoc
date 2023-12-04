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


def count_match(cards: List[Card]) -> List[int]:
    matches: List[int] = []
    for winning, numbers in cards:
        # Count matching number between the two lists.
        matches.append(sum(i in numbers for i in winning))
    return matches


def compute_points(matches: List[int]) -> List[int]:
    points: List[int] = []
    for match in matches:
        points.append(pow(2, match - 1) if match != 0 else 0)
    return points


def count_copy_cards(matches: List[int]) -> List[int]:
    count = len(matches)
    # At least, one card of each.
    copies: List[int] = [1] * count
    for i in range(0, count):
        # Win one card for each card owned.
        factor = copies[i]
        for j in range(1, matches[i] + 1):
            if i + j < count:
                copies[i + j] += factor
    return copies


def process(puzzle_in: List[str]):
    cards = parse_card(puzzle_in)
    matches = count_match(cards)
    print(f"Part 1: {sum(compute_points(matches))}")
    copies = count_copy_cards(matches)
    print(f"Part 2: {sum(copies)}")
