
def readfile(filename):
    rv = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            num = int(line)
            rv.append(num)
    return rv


def scandata(data, plen):
    for i in range(plen, len(data)):
        valid = False
        start = i-plen
        for j in range(start, i):
            for k in range(j, i):
                if data[j]+data[k] == data[i]:
                    valid = True
                    break
            if valid:
                break
        if not valid:
            return i


def find_contig_range(data, invalid):
    smallest = 999999999999
    largest = -smallest
    for i in range(len(data)):
        temp = invalid
        j = i
        while temp > 0:
            temp = temp - data[j]
            j = j+1
        if temp == 0 and j > 1:
            for k in range(i, j):
                if data[k] < smallest:
                    smallest = data[k]
                if data[k] > largest:
                    largest = data[k]
            return (smallest, largest)

    return (-1, -1)


def main():
    # (fn, plen) = ("test.txt", 5)
    (fn, plen) = ("input.txt", 25)
    data = readfile(fn)
    print(len(data))
    ipos = scandata(data, plen)
    invalid = data[ipos]
    print("Invalid = " + str(invalid))
    (smallest, largest) = find_contig_range(data, invalid)
    print("Answer = %d" % (smallest+largest))


if __name__ == "__main__":
    main()
