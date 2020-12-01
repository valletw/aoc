#! /usr/bin/env python3
import argparse


class Day23:
    """ Day 23: Category Six """
    def __init__(self, input_file):
        self.nb_computer = 50
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
        # Initialise network.
        computers = [Computer(data, i) for i in range(self.nb_computer)]
        first_nat_pkt = None
        y = 0
        nat_pkt = None
        while True:
            nb_idle = 0
            for i in range(self.nb_computer):
                c = computers[i]
                ret = c.exec()
                if ret > 0:
                    if ret == 255:
                        nb_idle += 1
                        continue
                    if c.has_received():
                        addr, pkt = c.read()
                        if addr == 255:
                            if first_nat_pkt is None:
                                first_nat_pkt = pkt
                            nat_pkt = pkt
                        else:
                            computers[addr].write(pkt)
            if nb_idle == 50 and nat_pkt is not None:
                # All computer are idle, send resume.
                computers[0].write(nat_pkt)
                if y == nat_pkt[1]:
                    break
                else:
                    y = nat_pkt[1]
        print(f"First NAT packet received: {first_nat_pkt}")
        print(f"First C0 Y value: {y}")


class Computer:
    def __init__(self, prog, addr, debug = False):
        self.prog = Intcode(prog)
        self.addr = addr
        self.debug = debug
        self.qin = list()
        self.qout = list()
        self.qin.append(self.addr)
        self.pdebug("initialised")

    def has_received(self):
        l = len(self.qout)
        return l != 0 and l % 3 == 0

    def read(self):
        addr = self.qout[0]
        pkt = self.qout[1:3]
        self.qout = self.qout[3:]
        self.pdebug(f"read @{addr:03d} pkt={pkt}")
        return addr, pkt

    def write(self, pkt):
        self.pdebug(f"write pkt={pkt}")
        self.qin.extend(pkt)

    def exec(self):
        self.pdebug(f"exec in={self.qin}")
        if len(self.qin) != 0:
            param = self.qin[0]
        else:
            param = -1
        stat, out = self.prog.exec(param)
        self.pdebug(f"exec stat={stat} out={out}")
        ret = stat
        if stat == 1:
            # New output parameter.
            self.qout.append(out)
        elif stat == 2 and param != -1:
            # Input parameter has been read.
            self.qin.pop(0)
        elif stat == 2 and param == -1:
            ret = 255
        return ret

    def pdebug(self, str):
        if self.debug:
            print(f"c{self.addr:03d} {str}")


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
        out_params = None
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
            if out_params is None:
                ret = 2
            else:
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
        self.cmd = f"{self.pc:04d}: in {dbg[0]}, {in_params}"
        self.cmd += f"    ; {args[0]}"
        self.memory[args[0]] = in_params
        # Move to next opcode.
        self.pc += 2
        return True

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
    parser.add_argument('input', help="File containing day 23 input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day23(args.input)
