#!/usr/bin/env python3
import argparse
import re


class Day4:
    """ Day 4: Passport Processing """
    _FIELD_RULES = {
        "byr" : {
            "format": re.compile(r"^(\d{4})$"),
            "min": 1920,
            "max": 2020
        },
        "iyr": {
            "format": re.compile(r"^(\d{4})$"),
            "min": 2010,
            "max": 2020
        },
        "eyr": {
            "format": re.compile(r"^(\d{4})$"),
            "min": 2020,
            "max": 2030
        },
        "hgt" : {
            "format": re.compile(r"^(\d+)(cm|in)$"),
            "unit": ["cm", "in"],
            "min": [150, 59],
            "max": [193, 76]
        },
        "hcl" : {
            "format": re.compile(r"^#([0-9a-f]{6})$")
        },
        "ecl" : {
            "format": re.compile(r"^([a-z]{3})$"),
            "match": ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        },
        "pid" : {
            "format": re.compile(r"^(\d{9})$")
        }
    }

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
        passport_valid_nb_1 = 0
        passport_valid_nb_2 = 0
        for passport in self._passports:
            field_nb = 0
            field_valid_nb = 0
            for field, value in passport.items():
                # Count the number of required field found.
                if field in self._FIELD_RULES.keys():
                    field_nb += 1
                    rules = self._FIELD_RULES[field]
                    extract = rules["format"].match(value)
                    if extract is not None:
                        if field in ["byr", "iyr", "eyr"]:
                            # Check year range.
                            year = int(extract.groups()[0])
                            if rules["min"] <= int(year) and int(year) <= rules["max"]:
                                field_valid_nb += 1
                        elif field == "hgt":
                            # Check size.
                            size = int(extract.groups()[0])
                            unit = extract.groups()[1]
                            if unit in rules["unit"]:
                                unit_id = rules["unit"].index(unit)
                                if rules["min"][unit_id] <= size and size <= rules["max"][unit_id]:
                                    field_valid_nb += 1
                        elif field == "ecl":
                            # Check color.
                            color = extract.groups()[0]
                            if color in rules["match"]:
                                field_valid_nb += 1
                        elif field in ["hcl", "pid"]:
                            # No additional test.
                            field_valid_nb += 1
            # Passport is valid only with all the required field.
            if field_nb == len(self._FIELD_RULES.keys()):
                passport_valid_nb_1 += 1
            # Passport is valid and all the required fields also.
            if field_valid_nb == len(self._FIELD_RULES.keys()):
                passport_valid_nb_2 += 1
        print(f"Part 1: {passport_valid_nb_1}")
        print(f"Part 2: {passport_valid_nb_2}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="File containing day input data")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Day4(args.input)
