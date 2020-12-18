

def process_rule(rules, line):
    parts = line.split(":")
    name = parts[0].strip()
    ranges = parts[1].split("or")
    rdat = []
    for r in ranges:
        r = r.strip()
        rp = r.split("-")
        low = int(rp[0])
        hi = int(rp[1])
        rdat.append((low, hi))
    rules.append([name, rdat])


def process_your_ticket(rules, line):
    parts = [int(p) for p in line.split(",")]
    return parts


def validate_num(rules, num):
    for rule in rules:
        for (low, hi) in rule[1]:
            if num >= low and num <= hi:
                return True
    return False


def process_nearby_ticket(rules, line):
    error = 0
    parts = [int(p) for p in line.split(",")]
    for num in parts:
        if not validate_num(rules, num):
            error = error + num
    if error == 0:
        return (error, parts)
    else:
        return (error, [])


def apply_rule(rule, num):
    for (low, hi) in rule[1]:
        if num >= low and num <= hi:
            return True
    return False


def scan_rules(rules, valid_tickets):
    data = []
    for rule in rules:
        hdrlen = len(rule[0])
        spaces = " "*(30-hdrlen)
        print(rule[0]+spaces, end="")
        row = []
        for column in range(len(valid_tickets[0])):
            rulegood = True
            for ticket in valid_tickets:
                if apply_rule(rule, ticket[column]) == False:
                    #print(rule, " failed on ", ticket[column])
                    rulegood = False
                    break
            row.append(int(rulegood))
            print("{} ".format(int(rulegood)), end="")
        print("")
        data.append(row)
    return data


def readdata(filename):
    rules = []  # format will be a tuple of (name, (range, range))
    RULE_MODE = 1
    YOUR_TICKET_MODE = 2
    NEARBY_TICKET_MODE = 3
    mode = RULE_MODE
    ser = 0
    valid_tickets = []
    my_ticket = None
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            if line == "your ticket:":
                mode = YOUR_TICKET_MODE
                print("processing your ticket")
                continue
            elif line == "nearby tickets:":
                mode = NEARBY_TICKET_MODE
                print("processing nearby tickets")
                continue
            if mode == RULE_MODE:
                process_rule(rules, line)
            elif mode == YOUR_TICKET_MODE:
                my_ticket = process_your_ticket(rules, line)
            elif mode == NEARBY_TICKET_MODE:
                (error, valid) = process_nearby_ticket(rules, line)
                if error > 0:
                    ser = ser + error
                else:
                    valid_tickets.append(valid)
    print("Scanning Error Rate {}".format(ser))
    print("{} valid tickets".format(len(valid_tickets)))
    data = scan_rules(rules, valid_tickets)
    field_cols = {}
    found_row = True
    while found_row:
        found_row = False
        for (i, row) in enumerate(data):
            if row.count(1) == 1:
                col = row.index(1)
                field_cols[rules[i][0]] = col
                print(rules[i][0], " has a unique column ", row.index(1))
                found_row = True
                for row in data:
                    row[col] = 0
                break
#    print(data)
    missing_row = ""
    for r in rules:
        if r[0] in field_cols:
            continue
        else:
            missing_row = r[0]
    print("Missing Row is ", missing_row)
    cols = {}
    for k, v in field_cols.items():
        cols[v] = k
    missing_col = -1
    for i in range(len(field_cols)):
        if i in cols:
            continue
        else:
            missing_col = i
    print("missing col", missing_col)
    field_cols[missing_row] = missing_col
    print(field_cols)
    print(len(rules), len(field_cols.keys()))
    answer = 1
    for (k, v) in field_cols.items():
        if k.startswith("departure"):
            print(my_ticket[v])
            answer = answer * my_ticket[v]
    print("Answer is ", answer)


def main():
    readdata("input.txt")


if __name__ == "__main__":
    main()
