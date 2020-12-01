#! /usr/bin/env python3
import argparse
import heapq


class Day15:
    """ Day 15: Oxygen System """
    def __init__(self, input_file):
        self.x_max = 50
        self.y_max = 50
        self.oxygen = (0, 0)
        self.grid = Grid(self.x_max, self.y_max,
            (self.x_max // 2, self.y_max // 2))
        self.dir_val = [1, 4, 2, 3]
        self.process(input_file)

    def process(self, input_file):
        list = {}
        data = []
        # Read all input data.
        with open(input_file, "r") as input:
            list = str(input.read()).split(",")
        # Convert input data to integer array.
        for i in list:
            data.append(int(i))
        # Initialise program, explore map to find oxygen system.
        prog = Intcode(data)
        x = self.grid.start[0]
        y = self.grid.start[1]
        dir = 0
        turn = False
        while True:
            stat, out = prog.exec(self.dir_val[dir])
            if stat == 0:
                break
            # Process output.
            if out == 0:
                # Hit wall.
                x1, y1 = self.update_coordinate(x, y, self.dir_val[dir])
                self.grid.walls.add((x1, y1))
            elif out == 1:
                # Move ok.
                x, y = self.update_coordinate(x, y, self.dir_val[dir])
                turn = True
            elif out == 2:
                # Find oxygen system.
                self.grid.goal = (x, y)
                break
            # Update direction.
            dir, turn = self.update_direction(x, y, dir, turn)
        # Find paths and there cost from start to oxygen system.
        find_path = False
        path = {}
        while not find_path:
            came_from, _ = self.a_star_search()
            path = self.reconstruct_path(came_from)
            # Execute program with this path, check if walls missing.
            prog = Intcode(data)
            for i in range(len(path) - 1):
                a = (path[i][0], path[i][1])
                b = (path[i + 1][0], path[i + 1][1])
                # Next point is goal, can stop.
                if b == self.grid.goal:
                    find_path = True
                    break
                # Update robot position.
                stat, out = prog.exec(self.get_direction(a, b))
                if stat == 0:
                    break
                if out == 0:
                    # Hit wall, need to find new path.
                    self.grid.walls.add(b)
                    break
                elif out == 2:
                    # Find oxygen system.
                    find_path = True
                    break
        print(f"Cost: {len(path)}")

    def update_direction(self, x, y, dir, turn = False):
        # Look on left if force turn.
        if turn:
            dir_l = dir - 1
            if dir_l == -1:
                dir_l = 3
            xl, yl = self.update_coordinate(x, y, self.dir_val[dir_l])
            if (xl, yl) not in self.grid.walls:
                dir = dir_l
                turn = False
        # Look in front.
        xf, yf = self.update_coordinate(x, y, self.dir_val[dir])
        if (xf, yf) in self.grid.walls:
            # Wall in front, go right.
            dir += 1
            dir %= 4
            turn = True
        return dir, turn

    def get_direction(self, a, b):
        dir = 0
        if a[0] < b[0]:
            # East.
            dir = 4
        elif a[0] > b[0]:
            # West.
            dir = 3
        else:
            if a[1] < b[1]:
                # South.
                dir = 2
            else:
                # North.
                dir = 1
        return dir

    def update_coordinate(self, x, y, dir):
        # Check direction.
        if dir == 1:
            # North.
            y -= 1
        elif dir == 2:
            # South.
            y += 1
        elif dir == 3:
            # West.
            x -= 1
        else:
            # East.
            x += 1
        return x, y

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
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self):
        start = self.grid.start
        goal = self.grid.goal
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
        return came_from, cost_so_far


class Grid:
    def __init__(self, width, height, start):
        self.width = width
        self.height = height
        self.walls = set()
        self.start = start
        self.goal = (0, 0)

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def print(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.walls:
                    s += str("#")
                elif (x, y) == self.start:
                    s += str("x")
                elif (x, y) == self.goal:
                    s += str("o")
                else:
                    s += str(" ")
            s += str("\n")
        print(s)

    def print_cost(self, cost):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.walls:
                    s += str("  # ")
                elif (x, y) == self.start:
                    s += str("  x ")
                elif (x, y) == self.goal:
                    s += str("  o ")
                elif (x, y) in cost:
                    s += f"{cost[(x, y)]:3d} "
                else:
                    s += str("    ")
            s += str("\n")
        print(s)
        return


class Intcode:
    """ Intcode program """
    def __init__(self, memory, debug = False):
        self.memory = memory.copy()
        self.memory.extend([0] * (5 * 1024))
        self.pc = 0
        self.rel = 0
        self.cmd = ""
        self.debug = debug

    def exec(self, in_params):
        out_params = 0
        halt = False
        pause = False
        while not halt and not pause and self.pc < len(self.memory):
            # Get opcode and mode.
            opcode = int(self.memory[self.pc] % 100)
            mode = [int(m) for m in str(int(self.memory[self.pc] / 100))]
            mode.reverse()
            if len(mode) < 3:
                mode.extend([0] * (3 - len(mode)))
            # Parse opcode.
            if opcode == 1:
                pause = self.inst_add(mode)
            elif opcode == 2:
                pause = self.inst_mul(mode)
            elif opcode == 3:
                pause = self.inst_stdin(mode, in_params)
            elif opcode == 4:
                pause, out_params = self.inst_stdout(mode)
            elif opcode == 5:
                pause = self.inst_cbnz(mode)
            elif opcode == 6:
                pause = self.inst_cbz(mode)
            elif opcode == 7:
                pause = self.inst_lt(mode)
            elif opcode == 8:
                pause = self.inst_eq(mode)
            elif opcode == 9:
                pause = self.inst_rel(mode)
            elif opcode == 99:
                halt = self.inst_halt(mode)
            # Print executed command.
            if self.debug:
                print(self.cmd)
        # Return program output.
        ret = 0
        if pause:
            ret = 1
        return ret, out_params

    def read_params(self, mode, nb):
        # Get arguments.
        args = []
        for j in range(1, nb + 1):
            args.append(self.memory[self.pc + j])
        # Check for mode.
        vals = []
        dbg = []
        for j in range(0, nb):
            # Position mode.
            if mode[j] == 0:
                vals.append(self.memory[args[j]])
                dbg.append(f"[{args[j]}]")
            # Immediate mode.
            elif mode[j] == 1:
                vals.append(args[j])
                dbg.append(f"{args[j]}")
            # Relative mode.
            else:
                vals.append(self.memory[self.rel + args[j]])
                dbg.append(f"[r{args[j]} ({self.rel + args[j]})]")
                args[j] += self.rel
        return args, vals, dbg

    def inst_add(self, mode):
        args, vals, dbg = self.read_params(mode, 3)
        self.cmd  = f"{self.pc:04d}: add {dbg[2]}, {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {args[2]}, {vals[0]}, {vals[1]}"
        self.memory[args[2]] = vals[0] + vals[1]
        # Move to next opcode.
        self.pc += 4
        return False

    def inst_mul(self, mode):
        args, vals, dbg = self.read_params(mode, 3)
        self.cmd  = f"{self.pc:04d}: mul {dbg[2]}, {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {args[2]}, {vals[0]}, {vals[1]}"
        self.memory[args[2]] = vals[0] * vals[1]
        # Move to next opcode.
        self.pc += 4
        return False

    def inst_stdin(self, mode, in_params):
        args, _, dbg = self.read_params(mode, 1)
        self.cmd  = f"{self.pc:04d}: in {dbg[0]}, {in_params}"
        self.cmd += f"    ; {args[0]}"
        self.memory[args[0]] = in_params
        # Move to next opcode.
        self.pc += 2
        return False

    def inst_stdout(self, mode):
        _, vals, dbg = self.read_params(mode, 1)
        self.cmd  = f"{self.pc:04d}: out {dbg[0]}"
        self.cmd += f"    ; {vals[0]}"
        # Move to next opcode.
        self.pc += 2
        return True, vals[0]

    def inst_cbnz(self, mode):
        _, vals, dbg = self.read_params(mode, 2)
        self.cmd  = f"{self.pc:04d}: cbnz {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {vals[0]}, {vals[1]}"
        if vals[0] != 0:
            # Move to value.
            self.pc = vals[1]
        else:
            # Move to next opcode.
            self.pc += 3
        return False

    def inst_cbz(self, mode):
        _, vals, dbg = self.read_params(mode, 2)
        self.cmd  = f"{self.pc:04d}: cbz {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {vals[0]}, {vals[1]}"
        if vals[0] == 0:
            # Move to value.
            self.pc = vals[1]
        else:
            # Move to next opcode.
            self.pc += 3
        return False

    def inst_lt(self, mode):
        args, vals, dbg = self.read_params(mode, 3)
        self.cmd  = f"{self.pc:04d}: lt {dbg[2]}, {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {args[2]}, {vals[0]}, {vals[1]}"
        if vals[0] < vals[1]:
            self.memory[args[2]] = 1
        else:
            self.memory[args[2]] = 0
        # Move to next opcode.
        self.pc += 4
        return False

    def inst_eq(self, mode):
        args, vals, dbg = self.read_params(mode, 3)
        self.cmd  = f"{self.pc:04d}: eq {dbg[2]}, {dbg[0]}, {dbg[1]}"
        self.cmd += f"    ; {args[2]}, {vals[0]}, {vals[1]}"
        if vals[0] == vals[1]:
            self.memory[args[2]] = 1
        else:
            self.memory[args[2]] = 0
        # Move to next opcode.
        self.pc += 4
        return False

    def inst_rel(self, mode):
        _, vals, dbg = self.read_params(mode, 1)
        self.cmd  = f"{self.pc:04d}: rel {dbg[0]}"
        self.cmd += f"    ; {vals[0]}"
        self.rel += vals[0]
        # Move to next opcode.
        self.pc += 2
        return False

    def inst_halt(self, mode):
        self.cmd = f"{self.pc:04d}: halt"
        return True


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day 15 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day15(args.input)
