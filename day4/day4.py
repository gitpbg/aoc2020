required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
optional_fields = ["cid"]
eye_colors = ["amb", "blu",  "brn", "gry",  "grn", "hzl", "oth"]


def validate_year(value, expected_length, lwr, upr):
    if len(value) != expected_length:
        return False
    try:
        year = int(value)
    except ValueError:
        return False
    if (year >= lwr and year <= upr):
        return True
    return False


def validate_height(value):
    try:
        (valnum, valtype) = (int(value[:-2]), value[-2:])
        if valtype == "cm" and (valnum >= 150 and valnum <= 193):
            return True
        elif valtype == "in" and (valnum >= 59 and valnum <= 76):
            return True
    except ValueError:
        pass
    return False


def validate_hair_color(value):
    if value[0] != "#":
        return False
    value = value[1:]
    if len(value) != 6:
        return False
    try:
        v = int(value, 16)
    except ValueError:
        return False
    return True


def validate_eye_color(value):
    return value in eye_colors


def validate_passport_id(value):
    if len(value) != 9:
        return False
    try:
        v = int(value)
    except ValueError:
        return False
    return True


def validate_field(name, value):
    if name == "byr":
        return validate_year(value, 4, 1920, 2002)
    elif name == "iyr":
        return validate_year(value, 4, 2010, 2020)
    elif name == "eyr":
        return validate_year(value, 4, 2020, 2030)
    elif name == "hgt":
        return validate_height(value)
    elif name == "hcl":
        return validate_hair_color(value)
    elif name == "ecl":
        return validate_eye_color(value)
    elif name == "pid":
        return validate_passport_id(value)
    return False


class Passport:

    def __init__(self):
        self.fields = {}

    def set_field(self, name, value):
        self.fields[name] = value

    def validate_passport(self):
        for key in required_fields:
            if key not in self.fields:
                return False
            if self.fields[key] is None:
                return False
            if self.fields[key].strip() == "":
                return False
            if not validate_field(key, self.fields[key]):
                return False
        return True

    def __str__(self):
        return str(self.fields)


def read_data(filename):
    rv = []
    currentPassport = None
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                if currentPassport is not None:
                    rv.append(currentPassport)
                    currentPassport = None
            else:
                if currentPassport is None:
                    currentPassport = Passport()
                fields = line.split(" ")
                for fld in fields:
                    nv = fld.split(":")
                    (name, value) = (nv[0], nv[1])
                    currentPassport.set_field(name, value)
        if currentPassport is not None:
            rv.append(currentPassport)
    f.close()
    return rv


def main():
    passports = read_data("input.txt")
    valid = 0
    for p in passports:
        if p.validate_passport():
            valid = valid + 1
    print("%d valid passports found" % (valid))


if __name__ == "__main__":
    main()
