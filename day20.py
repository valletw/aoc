#! /usr/bin/env python3
import argparse
import heapq


class Day20:
    """ Day 19: Tractor Beam """
    def __init__(self, input_file):
        self.grid = Grid()
        self.grid.load(input_file)
        self.process()

    def process(self):
        _, costs = self.a_star_search()
        print(f"Steps: {costs[self.grid.goal]}")
        self.grid.recursion_enable(True)
        _, costs = self.a_star_search()
        print(f"Steps (recursive): {costs[self.grid.goal]}")

    def reconstruct_path(self, came_from):
        start = self.grid.start
        goal = self.grid.goal
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path

    def heuristic(self, a, b):
        x1, y1, _ = a
        x2, y2, _ = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self):
        start = (self.grid.start[0], self.grid.start[1], 0)
        goal = (self.grid.goal[0], self.grid.goal[1], 0)
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
            for next, cost in self.grid.neighbors(current):
                new_cost = cost_so_far[current] + cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current
        return self.reconstruct_path(came_from), cost_so_far


class Grid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.start = (0, 0)
        self.goal = (0, 0)
        self.walls = set()
        self.voids = set()
        self.portals = dict()
        self.portals_outer = set()
        self.recursion_en = False

    def recursion_enable(self, en: bool):
        self.recursion_en = en

    def load(self, input_file):
        portals = dict()
        with open(input_file, "r") as input:
            self.height = 0
            for line in input:
                self.width = 0
                for s in line:
                    p = (self.width, self.height)
                    if s == ' ':
                        self.voids.add(p)
                    elif s == '#':
                        self.walls.add(p)
                    elif s in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        portals[p] = s
                    self.width += 1
                self.height += 1
        portals_done = []
        for p1, v in portals.items():
            if p1 in portals_done:
                continue
            x, y = p1
            entry = 0
            name = str(v)
            # Search portal name (2 letters).
            # Filter should leave only the 2nd letters, and may be the entry.
            # The portals are around void or grid edge.
            search = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            search = filter(self.in_bounds, search)
            search = filter(self.passable, search)
            search = [s for s in search]
            assert len(search) <= 2
            if len(search) == 1:
                # Only the 2nd letter available.
                name += str(portals[search[0]])
                p2 = search[0]
                # Find entry point, start search from position 2.
                search = [(p2[0] + 1, p2[1]), (p2[0] - 1, p2[1]),
                    (p2[0], p2[1] + 1), (p2[0], p2[1] - 1)]
                search = filter(self.in_bounds, search)
                search = filter(self.passable, search)
                search = [s for s in search]
                # Entry cannot be first position.
                if search[0] != p1:
                    entry = search[0]
                else:
                    entry = search[1]
            else:
                # 2nd letter and entry point are available.
                if search[0] in portals.keys():
                    name += str(portals[search[0]])
                    p2 = search[0]
                    entry = search[1]
                else:
                    name += str(portals[search[1]])
                    p2 = search[1]
                    entry = search[0]
            # Set portals positions as void.
            self.voids.add(p1)
            self.voids.add(p2)
            # Remove portals positions from temporay portals list.
            portals_done.extend([p1, p2])
            # Check if portal is already known.
            if name in self.portals.keys():
                # Portal is known, store entry on name key, and add translation.
                self.portals[name].append(entry)
                e = self.portals[name][0]
                self.portals[e] = entry
                self.portals[entry] = e
            else:
                # Portal not known yet, save entry point with name as key.
                self.portals[name] = [entry]
            # Check if entry is on outer.
            if entry[0] <= 2 or self.width - 4 <= entry[0] \
                or entry[1] <= 2 or self.height - 3 <= entry[1]:
                self.portals_outer.add(entry)
        # Get start and end position.
        self.start = self.portals['AA'][0]
        self.goal = self.portals['ZZ'][0]
        # Remove start and end position from outer portals.
        self.portals_outer.remove(self.start)
        self.portals_outer.remove(self.goal)

    def r_width(self):
        return range(self.width)

    def r_height(self):
        return range(self.height)

    def teleport(self, a):
        if a in self.portals.keys():
            return self.portals[a]
        else:
            return a

    def in_bounds(self, a):
        try:
            x, y, _ = a
        except ValueError:
            x, y = a
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, a):
        try:
            x, y, lvl = a
        except ValueError:
            x, y = a
            lvl = 0
        p = (x, y)
        if self.recursion_en:
            if lvl == 0:
                # Top level: Outer portals are walls.
                return p not in self.walls | self.voids | self.portals_outer
            else:
                # Outermost level: Start and end position are walls.
                return p not in self.walls | self.voids | self.start | self.goal
        else:
            return p not in self.walls | self.voids

    def neighbors(self, p):
        x, y, lvl = p
        search = [(x + 1, y, lvl), (x, y - 1, lvl),
            (x - 1, y, lvl), (x, y + 1, lvl)]
        if (x + y) % 2 == 0:
            search.reverse() # aesthetics
        search = filter(self.in_bounds, search)
        search = filter(self.passable, search)
        results = []
        for s in search:
            x, y, lvl = s
            if (x, y) in self.portals.keys():
                # Teleport to other portal, cost 2.
                portal = self.portals[(x, y)]
                if self.recursion_enable:
                    if (x, y) in self.portals_outer:
                        lvl -= 1
                    else:
                        lvl += 1
                else:
                    lvl = 0
                results.append(((portal[0], portal[1], lvl), 2))
            else:
                # No teleportation, cost 1.
                results.append(((x, y, lvl) , 1))
        return results

    def print(self):
        s = ""
        for y in self.r_height():
            for x in self.r_width():
                if (x, y) in self.walls:
                    s += str('#')
                elif (x,y) in self.voids:
                    s += str('.')
                elif (x,y) == self.start:
                    s += str('S')
                elif (x,y) == self.goal:
                    s += str('E')
                elif (x,y) in self.portals.keys():
                    s += str('O')
                else:
                    s += str(' ')
            s += str("\n")
        print(s)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 20 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day20(args.input)
