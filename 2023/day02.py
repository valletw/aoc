from typing import List, Tuple


CUBES = Tuple[int, int, int]
GAMES = List[List[CUBES]]
R = 0
G = 1
B = 2


def extract_games(puzzle_in: List[str]) -> GAMES:
    games: GAMES = []
    # Parse each line.
    for line in puzzle_in:
        # Generate empty subsets list.
        games.append([])
        # Extract sets from the game.
        sets = line.split(":")[1].rstrip()
        # Extract subsets from the game.
        subsets = sets.split(";")
        # Parse each subsets.
        for subset in subsets:
            cube: CUBES = (0, 0, 0)
            # Extract cubes.
            cubes = subset.strip().split(",")
            # Parse each cubes for detail.
            for c in cubes:
                nb, colour = c.strip().split(" ")
                if colour == "red":
                    cube = (int(nb), cube[1], cube[2])
                elif colour == "green":
                    cube = (cube[0], int(nb), cube[2])
                elif colour == "blue":
                    cube = (cube[0], cube[1], int(nb))
            # Add cube to game.
            games[-1].append(cube)
    return games


def check_combinaison(
        games: GAMES, red: int, green: int, blue: int) -> List[int]:
    game_valid: List[int] = []
    game_id = 1
    # Parse each games.
    for game in games:
        # Parse each cube to find invalid combinaison.
        valid = True
        for cubes in game:
            if cubes[R] > red or cubes[G] > green or cubes[B] > blue:
                valid = False
        # If valid combinaison, add game ID.
        if valid:
            game_valid.append(game_id)
        game_id += 1
    return game_valid


def minimal_cubes_set(games: GAMES) -> List[int]:
    powers: List[int] = []
    # Parse each games.
    for game in games:
        # Find maximum value for each cube to determine minimal set.
        r_max = 0
        g_max = 0
        b_max = 0
        for cubes in game:
            if cubes[R] > r_max:
                r_max = cubes[R]
            if cubes[G] > g_max:
                g_max = cubes[G]
            if cubes[B] > b_max:
                b_max = cubes[B]
        # Compute power of the combinaison.
        powers.append(r_max * g_max * b_max)
    return powers


def process(puzzle_in: List[str]):
    games = extract_games(puzzle_in)
    games_valid = check_combinaison(games, 12, 13, 14)
    print(f"Part 1: {sum(games_valid)}")
    powers = minimal_cubes_set(games)
    print(f"Part 2: {sum(powers)}")
