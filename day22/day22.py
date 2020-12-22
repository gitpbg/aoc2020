
def readdata(filename):
    p1 = []
    p2 = []
    curdeck = None
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            if line.startswith("Player 1"):
                curdeck = p1
            elif line.startswith("Player 2"):
                curdeck = p2
            else:
                curdeck.append(int(line))
    return p1, p2


gamenum = 0


def playgame(d1, d2):
    global gamenum
    turns = 100000000
    turn = 0
    gamenum = gamenum + 1
    curgame = gamenum
    outcomes = {}
    print("Game {} starting with P1 {} P2 {}".format(curgame, str(d1), str(d2)))
    while len(d1) != 0 and len(d2) != 0:
        #print("Game ", curgame, "Turn ", turn+1, "P1", d1, "P2", d2)
        tmp = (tuple(d1), tuple(d2))
        if tmp in outcomes:
            print("Deck Found in outcomes returning win for p1, See game ",
                  outcomes[tmp])
            return [1], []
        outcomes[tmp] = True
        c1 = d1[0]
        c2 = d2[0]
        d1 = d1[1:]
        d2 = d2[1:]
        recurse = False
        if c1 <= len(d1) and c2 <= len(d2):
            print("Playing Subgame to determine winner")
            t1, t2 = playgame(list(d1[0:c1]), list(d2[0:c2]))
            if len(t1) > len(t2):
                print("p1 won subgame")
                d1.append(c1)
                d1.append(c2)
            else:
                print("p2 won subgame")
                d2.append(c2)
                d2.append(c1)
            recurse = True
        if not recurse:
            if c1 > c2:
                d1.append(c1)
                d1.append(c2)
            elif c2 > c1:
                d2.append(c2)
                d2.append(c1)
            else:
                print("Cards are equal")
        # print(d1, d2)
        turn = turn + 1
        if turn > turns:
            break
    print("Game {} done in {} turns".format(curgame,  turn))
    return d1, d2


def main():
    global gamenum
    gamenum = 0
    d1, d2 = readdata("input.txt")
    print(d1, d2)
    d1, d2 = playgame(d1, d2)
    print("d1 = ", d1)
    print("d2 = ", d2)
    if len(d1) > 0:
        curdeck = d1
    else:
        curdeck = d2
    mpl = len(curdeck)
    sum = 0
    for num in curdeck:
        sum = sum + num * mpl
        mpl = mpl - 1
    print(sum)


if __name__ == "__main__":
    main()
