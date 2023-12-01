from typing import List, Optional


def parse(puzzle_in: List[str]) -> int:
    digit: List[int] = []
    # Parse all lines.
    for line in puzzle_in:
        first: Optional[str] = None
        last: Optional[str] = None
        # Parse all characters in line.
        for c in line:
            # Check if it is an integer.
            # Store first digit if not set, and update each time last.
            if c >= '0' and c <= '9':
                if first is None:
                    first = c
                else:
                    last = c
        # Check if digits has been found and concatenate them.
        # If no second digit, use the first one.
        assert first is not None
        if last is None:
            last = first
        digit.append(int(first + last))
    # Compute the sum of all digits.
    return sum(digit)


def process(puzzle_in: List[str]):
    print(f"Part 1: {parse(puzzle_in)}")
