from typing import List, Dict, Tuple


def parse(puzzle_in: List[str]) -> List[str]:
    sequences: List[str] = []
    for line in puzzle_in:
        sequences.extend(line.split(","))
    return sequences


def hash_algo(sequence: str) -> int:
    count = 0
    for c in sequence:
        count += ord(c)
        count *= 17
        count %= 256
    return count


def hashmap_algo(sequences: List[str]) -> int:
    boxes: Dict[int, List[Tuple[str, int]]] = {}
    # Assign lenses to boxes.
    for s in sequences:
        equal = s.split("=")
        # Check if equal operation.
        if len(equal) == 2:
            label, lid = equal
            bid = hash_algo(label)
            # Add box if not present.
            if bid not in boxes:
                boxes[bid] = []
            # Check if lense is already present either add it.
            found = False
            for idx, lense in enumerate(boxes[bid]):
                if lense[0] == label:
                    boxes[bid][idx] = (label, int(lid))
                    found = True
                    break
            if not found:
                boxes[bid].append((label, int(lid)))
        # Not equal, so it is dash operation.
        else:
            label = s[:-1]
            bid = hash_algo(label)
            # Add box if not present.
            if bid not in boxes:
                boxes[bid] = []
            # Remove label from box.
            boxes[bid] = list(filter(lambda a: a[0] != label, boxes[bid]))
    # Compute focusing power.
    power = 0
    for bid, lenses in boxes.items():
        for slot, lense in enumerate(lenses):
            power += (bid + 1) * (slot + 1) * lense[1]
    return power


def process(puzzle_in: List[str]):
    sequences = parse(puzzle_in)
    print(f"Part 1: {sum(hash_algo(s) for s in sequences)}")
    print(f"Part 2: {hashmap_algo(sequences)}")
