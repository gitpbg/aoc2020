import re
dbgprint = False
LAST = 0


def readdata1(filename):
    rules = []
    testdata = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            colonpos = line.find(":")
            if colonpos == -1:
                testdata.append(line)
            else:
                rulenum = int(line[:colonpos])
                ruleparts = line[colonpos+1:].strip()
                if "|" in ruleparts:
                    ruleparts = "(" + ruleparts+")"
                rules.append([rulenum, ruleparts])
    return (rules, testdata)


def check_for_digits(s):
    for ch in s:
        if ch == "|":
            continue
        if ch == " ":
            continue
        if ch.isdigit():
            return True
    return False


def rules_to_re(rules):
    rulemap = {}
    keepgoing = True
    while True:
        newadditions = False
        for (rulenum, ruleparts) in rules:
            if rulenum in rulemap:
                continue
            if check_for_digits(ruleparts) == False:
                print("Adding Rule to Map")
                rulemap[rulenum] = ruleparts.replace("\"", "")
                newadditions = True
        if newadditions == False:
            break
        for i in range(len(rules)):
            for k in rulemap.keys():
                sk = str(k)
                if sk in rules[i][1]:
                    rules[i][1] = rules[i][1].replace(sk, rulemap[k])
                    print("Rule ", i, " updated to ", rules[i][1])
    for i in range(len(rules)):
        if rules[i][0] == 0:
            rules[i][1] = rules[i][1].replace(' ', '')
            print("Rule 0:", rules[i][1])
            return rules[i][1]

    return "ERROR"


def firstsol():
    (rules, tests) = readdata("input.txt")
    print("Rules ", rules)
    print("Tests", tests)
    restr = rules_to_re(rules)
    print("Got ", restr)
    rex = re.compile(restr)
    sum = 0
    print(len(tests))
    for t in tests:
        if rex.match(t) is not None:
            t = rex.sub("HELLO", t)
            if t == "HELLO":
                print("Exact Match Found ", t)
                sum = sum+1
    print("Answer ", sum)


def istuple(v):
    return type(v) == type(())


MEMO = {}


def match(rules, rulenum, s, depth=0):
    k = (rulenum, s)
#    if k in MEMO:
#        return MEMO[k]
    prefix = ""
    if dbgprint:
        prefix = "  "*depth
        print(prefix + "match called ", rulenum, rules[rulenum], s)
    depth = depth+1
    if s == "" and rulenum == 31:
        return (False, 0)
    if s == "":
        print(prefix + "Called with Empty String and Rule ", rulenum)
        return False, 0
    if type(rules[rulenum]) == str:
        r = rules[rulenum]
        res = s[0] in r
        if dbgprint:
            print(prefix, "terminal [", r, "] returning ", res)
        return res, 1
    else:
        for t in rules[rulenum]:
            all = True
            pos = 0
            for idx in range(len(t)):
                (ok, adv) = match(rules, t[idx], s[pos:], depth)
                if ok and t[idx] == 42 and s[pos+adv:] == "":
                    print("OK HERE rule ", t[idx], t)
#                if s[pos:] == "" and idx+1 == len(t) and t[idx] in (31, 42) and (ok == False):
#                    print("Special case terminal pass for rules 31 and 42")
#                    ok = True
                all = all and ok
                if not ok:
                    break
                pos = pos + adv
            if all:
                tmp = (rulenum, s)
                MEMO[tmp] = (all, pos)
                if dbgprint:
                    print(prefix, "match found, returning True", pos, rulenum)
                return all, pos
        if dbgprint:
            print(prefix, "returning False for ", rulenum, depth-1)
        return False, 0


def match2(rules, rulenum, s, depth=0):
    global dbgprint
    global LAST
    if dbgprint == 1:
        print("Match Called for rulenum=", rulenum,
              " R=", rules[rulenum], " for s=", s, " depth = ", depth)
    # if DEBUG == 1 and (rulenum == 31 and s == ""):
    #     return (False, "")
    # if rulenum == 42 and LAST == 31 and s == "":
    #     print("GOT IT")
    #     return (False, "")
    # if (rulenum in (14, 1)) and s == "":
    #     if (LAST == 31 and rulenum == 14):
    #         return (False, "")
    #     return (True, "")
    LAST = rulenum

    if istuple(rules[rulenum]):
        for t in rules[rulenum]:
            rest = s
            lt = len(t)
            for (i, r) in enumerate(t):
                (ok, rest) = match(rules, r, rest, depth+1)
                if rest == "":
                    if i+1 == lt:  # match on the last rule
                        return (ok, rest)
                    else:
                        print(
                            "breaking string finished mid test [{}] rest=[{}]".format(s, rest))
                        break

                    # if ok and rest == "" and (rulenum in [14, 1]):
                    #     print("Rule ", r)
                    #     print("s = ", s)
                    #     return (ok, rest)
                if not ok:
                    break
            if ok:
                return ok, rest
    else:
        try:
            if rules[rulenum] == s[0]:
                return (True, s[1:])
        except IndexError:
            print("IndexError")
            return (True, "")
    return (False, "")


def readdata(filename):
    rules = {}
    tests = []
    readrules = True

    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                readrules = False
                continue
            if readrules:
                parts = line.split(":")
                rulenum = int(parts[0])
                if "|" in parts[1]:
                    dependents = parts[1].split("|")
                    rps = []
                    for d in dependents:
                        nums = map(lambda x: int(x), d.split())
                        rps.append(tuple(nums))
                    rules[rulenum] = tuple(rps)
                else:
                    if "\"" in parts[1]:
                        rules[rulenum] = parts[1].replace("\"", "").strip()
                    else:
                        rules[rulenum] = (tuple(
                            map(lambda x: int(x), parts[1].split())),)
            else:
                tests.append(line)
    return rules, tests


def main():
    global dbgprint
    good = ["bbabbbbaabaabba",
            "babbbbaabbbbbabbbbbbaabaaabaaa",
            "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
            "bbbbbbbaaaabbbbaaabbabaaa",
            "bbbababbbbaaaaaaaabbababaaababaabab",
            "ababaaaaaabaaab",
            "ababaaaaabbbaba",
            "baabbaaaabbaaaababbaababb",
            "abbbbabbbbaaaababbbbbbaaaababb",
            "aaaaabbaabaaaaababaa",
            "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
            "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"
            ]
    rules, tests = readdata("test3.txt")
    ork = list(rules.keys())
    ork.sort()

    # print(rules)
    # print(tests)
    rules[8] = ((42,), (42, 8))
    rules[11] = ((42, 31), (42, 11, 31))
    for rulenum in ork:
        print("Rule num=", rulenum, " r=", rules[rulenum])
    sum = 0
    for t in tests:
        #        if t not in good:
        #            continue
        print(t)
        (ok, adv) = match(rules, 0, t)
        print(ok, adv, t)
        x = t[adv:]
        print(ok, adv, len(t), "x=", x)
        if ok and t not in good:
            print("FALSE PASS", t)
            dbgprint = True
            print(dbgprint)
            (ok, adv) = match(rules, 0, t)
            print(dbgprint)
            dbgprint = False
            break
        if ok:
            sum = sum + 1
    # print(MEMO)
    print(sum)


if __name__ == "__main__":
    main()
