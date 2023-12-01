from typing import List, Optional


def digit_replace(puzzle_in: List[str]) -> List[str]:
    output: List[str] = []
    search_replace = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    for line in puzzle_in:
        # Find a digit-letter before the first true digit.
        i = 0
        while not line[i].isdigit():
            for search, replace in search_replace.items():
                if line[i:].startswith(search):
                    line = line.replace(search, replace, 1)
                    break
            i += 1
        # Find a digit-letter before the last true digit (reverse parsing).
        i = len(line) - 1
        while not line[i].isdigit():
            for search, replace in search_replace.items():
                if line[i:].startswith(search):
                    line = line.replace(search, replace, 1)
                    break
            i -= 1
        output.append(line)
    return output


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
            if c.isdigit():
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
    print(f"Part 2: {parse(digit_replace(puzzle_in))}")
