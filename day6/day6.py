

def make_new_group():
    # return [False for i in range(26)]
    return [0 for i in range(26)]


def main():
    f = open("input.txt", "r")
    curgroup = None
    total = 0
    numingroup = 0
    for line in f.readlines():
        line = line.strip()
        if line == "":
            if curgroup is not None:
                count = curgroup.count(numingroup)
                total = total + count
                curgroup = None
                numingroup = 0
        else:
            if curgroup is None:
                curgroup = make_new_group()
            numingroup = numingroup + 1
            for ch in line:
                index = ord(ch) - ord('a')
                curgroup[index] = curgroup[index] + 1

    if curgroup is not None:
        count = curgroup.count(numingroup)
        total = total + count

    print("Total is ", total)


if __name__ == "__main__":
    main()
