

def readdata(filename):
    rules = {}
    tests = []

    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            # print(line)
            pos = line.find(":")
            if pos >= 0:
                rulenum = int(line[:pos])
                rulepart = line[pos+1:]
                if rulepart.find("\"") >= 0:
                    rules[rulenum] = rulepart.strip().replace("\"", "")
                else:
                    parts = rulepart.split("|")
                    rulelist = []
                    for p in parts:
                        p = [int(v) for v in p.split()]
                        rulelist.append(tuple(p))
                    #print(rulenum, rulelist)
                    rules[rulenum] = tuple(rulelist)
            else:
                tests.append(line)
    return (rules, tests)


def match_rule(rules, rulenum, s):
    DEBUG = False
    rule = rules[rulenum]
    if DEBUG:
        print("Matching", rule)
    if s == "":
        print("Got Empty String while matching ", rulenum)
        return False, ""
    if type(rule) is str:
        if s[0] == rule:
            return (True, s[1:])
    else:
        for clauses in rule:
            rest = s
            last = clauses[-1]
            ok = False
            for clause in clauses:
                before = rest
                (ok, rest) = match_rule(rules, clause, rest)
                #
                # This was the most important line for part 2
                # What it means is the following:
                # Rule 11 is defined as (42, 31) or (42, 11, 31)
                # When we get to the 31 in the 2nd clause - rule 11 would have already consumed the string
                # so rule 11 is true and yet by testing an empty string we would call it false
                # so we have to short cut the looping here and declare a pass
                # to the if below means:
                # if the previous clause was 11, the last clause is 31 and the string has been consumed
                # then the match is correct and so return a True and empty string
                #
                # This was a hard one to crack and took me 6 days!!!!
                if clause == 11 and last == 31 and rest == "":
                    break
                if not ok:
                    break
            if ok:
                return (True, rest)
    return (False, "")


def match(rules, s):
    (ok, rest) = match_rule(rules, 0, s)
#    return ok and rest==""
    if ok and rest == "":
        return True
    return False


def main():
    rules, tests = readdata("input.txt")
    part = 2
    # print(rules)
    # print(tests)
    if part == 2:
        rules[8] = ((42,), (42, 8))
        rules[11] = ((42, 31), (42, 11, 31))
    count = 0
    for t in tests:
        result = match(rules, t)
        print(t, result)
        if result == True:
            count = count + 1
    print("{} strings matched".format(count))


if __name__ == "__main__":
    main()
