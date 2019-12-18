#! /usr/bin/env python3
import argparse
import heapq


class Day18:
    """ Day 18: Many-Worlds Interpretation """
    def __init__(self, input_file):
        self.grid = Grid()
        self.process(input_file)

    def process(self, input_file):
        start = (0, 0)
        # Read all input data.
        with open(input_file, "r") as input:
            y = 0
            for line in input:
                x = 0
                for s in line:
                    if s == '#':
                        self.grid.walls.add((x, y))
                    elif s == '@':
                        start = (x ,y)
                    elif s != '.':
                        i = ord(s)
                        if ord('a') <= i and i <= ord('z'):
                            # It is a key.
                            i -= ord('a')
                            self.grid.goals["keys"][i] = (x ,y)
                            self.grid.goals["keys_count"] += 1
                        elif ord('A') <= i and i <= ord('Z'):
                            # It is a door.
                            i -= ord('A')
                            self.grid.goals["doors"][i] = (x ,y)
                    x += 1
                self.grid.width = x
                y += 1
            self.grid.height = y
        # Find all keys, each time take the closest.
        steps = 0
        while True:
            paths = []
            # Get path to each keys available to find the best.
            for k in range(26):
                goal = self.grid.get_key_pos(k)
                if goal != 0:
                     path = self.a_star_search(start, goal)
                     if len(path) != 0:
                        paths.append((path, len(path), k))
            # Check if multiple path cross over to find multiple keys.
            keys = []
            if len(paths) > 1:
                paths.sort(reverse=True)
                min_path = min(paths, key = lambda p: p[1])
                # Compare path N and N+1 to get a match.
                keys_found = []
                keys_crossed = [(paths[0][1], paths[0][2])]
                for curr, next in zip(paths[:-1], paths[1:]):
                    curr_path = curr[0]
                    next_path = next[0]
                    if curr_path[:len(next_path)] == next_path:
                        # Two paths cross over.
                        keys_crossed.append((next[1], next[2]))
                    else:
                        # No paths crossed, prepare next round.
                        keys_found.append(keys_crossed)
                        keys_crossed = [(curr[1], curr[2])]
                # Last crossed path not yet added.
                keys_found.append(keys_crossed)
                # Find path with maximum keys found.
                keys = []
                for k in keys_found:
                    if len(keys) < len(k):
                        keys = k
                keys.sort()
                # Minimum path could be better than getting multiple keys.
                if min_path[1] < (keys[-1][0] // len(keys)):
                    keys = [(min_path[1], min_path[2])]
            else:
                # Only one path available.
                keys = [(paths[0][1], paths[0][2])]
            # Update keys available, and update start position (on key).
            for s, k in keys:
                start = self.grid.key_found(k)
                best_path = s
            # Increment number of steps.
            steps += best_path
            # Check if all keys as been found.
            if not self.grid.has_key_left():
                break
        print(f"Steps: {steps}")

    def reconstruct_path(self, start, goal, came_from):
        current = goal
        path = []
        # Path not complete (doors on the way).
        if goal in came_from:
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start) # optional
            path.reverse() # optional
        return path

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while len(frontier) != 0:
            current = heapq.heappop(frontier)[1]
            if current == goal:
                break
            for next in self.grid.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current
        return self.reconstruct_path(start, goal, came_from)


class Grid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.walls = set()
        self.goals = dict(
            keys = list([0] * 26),
            keys_count = 0,
            doors = list([0] * 26)
        )

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls and id not in self.goals["doors"]

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def key_found(self, id):
        # Key is found, remove door.
        self.goals["doors"][id] = 0
        # Update keys available, and return position.
        key_pos = self.goals["keys"][id]
        self.goals["keys"][id] = 0
        self.goals["keys_count"] -= 1
        print(f"Open {str(chr(id + ord('A')))} {key_pos}")
        return key_pos

    def has_key_left(self):
        return self.goals["keys_count"] != 0

    def get_key_pos(self, id):
        return self.goals["keys"][id]

    def print(self, start=None):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.walls:
                    # Walls.
                    s += str("#")
                elif (x, y) in self.goals["keys"]:
                    # Keys.
                    s += str(chr(ord('a') + self.goals["keys"].index((x, y))))
                elif (x, y) in self.goals["doors"]:
                    # Doors.
                    s += str(chr(ord('A') + self.goals["doors"].index((x, y))))
                elif start is not None and (x, y) == start:
                    # Position.
                    s += str("@")
                else:
                    # Open space.
                    s += str(" ")
            s += str("\n")
        print(s)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 18 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day18(args.input)
