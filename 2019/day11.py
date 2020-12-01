#! /usr/bin/env python3
import argparse
import array


class Day11:
    """ Day 11: Space Police """
    def __init__(self, input_file):
        self.width = 100
        self.height = 110
        self.grid1 = [[0] * self.width for i in range(self.height)]
        self.grid2 = [[1] * self.width for i in range(self.height)]
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
        # Initialise program, and set robot at center of the grid.
        prog = Intcode(data)
        robot_x = self.width // 2
        robot_y = self.height // 2
        robot_dir = 0
        # Start program.
        painted = set()
        halt = False
        while not halt:
            in_data = self.grid1[robot_y][robot_x]
            # Execute program to get new panel value.
            stat, panel = prog.exec(in_data)
            # Execute program to get new direction.
            stat, direction = prog.exec(in_data)
            if stat == 0:
                # Stop robot if program halt.
                halt = True
            else:
                # Store the painted panels.
                if in_data != panel:
                    painted.add((robot_x, robot_y))
                # Set new panel color.
                self.grid1[robot_y][robot_x] = panel
                # Update robot direction.
                if direction == 0:
                    # Turn 90° left.
                    if robot_dir == 0:
                        robot_dir = 3
                    else:
                        robot_dir -= 1
                else:
                    # Turn 90° right.
                    robot_dir += 1
                    robot_dir %= 4
                # Update robot position.
                if robot_dir == 0:
                    # Go up.
                    robot_y -= 1
                elif robot_dir == 1:
                    # Go right.
                    robot_x += 1
                elif robot_dir == 2:
                    # Go down.
                    robot_y += 1
                else:
                    # Go left.
                    robot_x -= 1
        print(f"Painted panel: {len(painted)}")
        # Initialise program, and set robot at center of the grid.
        prog = Intcode(data)
        robot_x = self.width // 2
        robot_y = self.height // 2
        robot_dir = 0
        # Start program.
        halt = False
        while not halt:
            in_data = self.grid2[robot_y][robot_x]
            # Execute program to get new panel value.
            stat, panel = prog.exec(in_data)
            # Execute program to get new direction.
            stat, direction = prog.exec(in_data)
            if stat == 0:
                # Stop robot if program halt.
                halt = True
            else:
                # Set new panel color.
                self.grid2[robot_y][robot_x] = panel
                # Update robot direction.
                if direction == 0:
                    # Turn 90° left.
                    if robot_dir == 0:
                        robot_dir = 3
                    else:
                        robot_dir -= 1
                else:
                    # Turn 90° right.
                    robot_dir += 1
                    robot_dir %= 4
                # Update robot position.
                if robot_dir == 0:
                    # Go up.
                    robot_y -= 1
                elif robot_dir == 1:
                    # Go right.
                    robot_x += 1
                elif robot_dir == 2:
                    # Go down.
                    robot_y += 1
                else:
                    # Go left.
                    robot_x -= 1
        s = ""
        for line in self.grid2:
            for col in line:
                if col == 1:
                    s += str('#')
                else:
                    s += str(' ')
            s += str('\n')
        print(s)


class Intcode:
    """ Intcode program """
    def __init__(self, memory, debug = False):
        self.memory = memory.copy()
        self.memory.extend([0] * (5 * 1024))
        self.pc = 0
        self.rel = 0
        self.input_id = 0
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
    parser.add_argument('input', help="File containing day 11 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day11(args.input)
