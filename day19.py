#! /usr/bin/env python3
import argparse
import math


class Day19:
    """ Day 19: Tractor Beam """
    def __init__(self, input_file):
        self.grid = Grid()
        self.data = []
        self.ship_size = 100
        self.process(input_file)

    def process(self, input_file):
        list = {}
        # Read all input data.
        with open(input_file, "r") as input:
            list = str(input.read()).split(",")
        # Convert input data to integer array.
        for i in list:
            self.data.append(int(i))
        # Parse each grid position.
        for y in self.grid.r_height():
            for x in self.grid.r_width():
                # Initialise program, and get drone status.
                _, out = Intcode(self.data).exec([x, y])
                if out == 1:
                    self.grid.beams.add((x, y))
        print(f"Points affected: {len(self.grid.beams)}")
        # Part 2: follow left line until (X+100, Y-100) fit.
        # Start from bottom left point.
        (x, y) = self.grid.beams_width()
        # Get x increment ratio.
        xr = x / 50
        # Do first increment (+100).
        x += int(xr * 50)
        y += 50
        while True:
            x = self.adjust_x(x, y)
            # Check top right corner ship position.
            _, out = Intcode(self.data).exec([
                x + self.ship_size, y - self.ship_size])
            if out == 1:
                # Adjust until the top right corner is on edge.
                top = 1
                right = 1
                while top == 1 or right == 1:
                    _, top = Intcode(self.data).exec([
                        x + self.ship_size    , y - self.ship_size - 1])
                    _, right = Intcode(self.data).exec([
                        x + self.ship_size + 1, y - self.ship_size])
                    if top == 1 or right == 1:
                        y -= 1
                        x = self.adjust_x(x, y)
                break
            else:
                # Corner not in beam shape, move to next position.
                x += int(xr * self.ship_size)
                y += self.ship_size
        # Ship fit in beam shape, get closest position (top left corner).
        y -= self.ship_size
        print(f"Ship position: {x * 10000 + y}")

    def adjust_x(self, x, y):
        ignore_next = False
        # Check the x position on left, shall be outside the beam shape.
        out = 1
        while out == 1:
            _, out = Intcode(self.data).exec([x - 1, y])
            if out == 1:
                # Left position inside, move left.
                x -= 1
                # Ignore next verification, position will be OK.
                ignore_next = True
        # Check the current x position, shall be inside the beam shape.
        if not ignore_next:
            out = 0
            while out == 0:
                _, out = Intcode(self.data).exec([x, y])
                if out == 0:
                    # Position outside, move right.
                    x += 1
        return x


class Grid:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.beams = set()

    def r_width(self):
        return range(self.width)

    def r_height(self):
        return range(self.height)

    def beams_width(self, height=None):
        if height is None:
            y = self.height - 1
        else:
            y = height
        first = None
        for x in self.r_width():
            if (x, y) in self.beams:
                first = (x, y)
                break
        return first

    def print(self):
        s = ""
        for y in self.r_height():
            for x in self.r_width():
                if (x, y) in self.beams:
                    s += str('#')
                else:
                    s += str('.')
            s += str("\n")
        print(s)


class Intcode:
    """ Intcode program """
    def __init__(self, memory, debug = False):
        self.memory = memory.copy()
        self.memory.extend([0] * (5 * 1024))
        self.pc = 0
        self.rel = 0
        self.cmd = ""
        self.debug = debug
        self.input_id = 0

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
        self.cmd  = f"{self.pc:04d}: in {dbg[0]}, {in_params[self.input_id]}"
        self.cmd += f"    ; {args[0]}"
        self.memory[args[0]] = in_params[self.input_id]
        self.input_id += 1
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
    parser.add_argument('input', help="File containing day 19 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day19(args.input)
