#!/usr/bin/env python3
import argparse


class Day4:
    """ Day 4: Passport Processing """
    _FIELD_REQ = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    def __init__(self, input_file):
        self._passports = list()
        self.process(input_file)

    def process(self, input_file):
        with open(input_file, "r") as input:
            fields = str()
            for line in input:
                line = line.rstrip()
                if line == "":
                    if len(fields) > 0:
                        # All field found, insert to passport database.
                        # Format as "JSON" to evaluate as dictionary.
                        fields_format = "{"
                        for field in fields.split(" "):
                            field_split = field.split(":")
                            if len(field_split) == 2:
                                fields_format += f"'{field_split[0]}':'{field_split[1]}',"
                        fields_format += "}"
                        self._passports.append(eval(fields_format))
                    # Clear fields.
                    fields = ""
                fields += line + " "
        # Parse passport.
        passport_valid_nb = 0
        for passport in self._passports:
            field_nb = 0
            for field in passport.keys():
                # Count the number of required field found.
                if field in self._FIELD_REQ:
                    field_nb += 1
            # Passport is valid only with all the required field.
            if field_nb == len(self._FIELD_REQ):
                passport_valid_nb += 1
        print(f"Part 1: {passport_valid_nb}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day4(args.input)
