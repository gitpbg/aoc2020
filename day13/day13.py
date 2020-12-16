from functools import reduce


def str_to_int(s):
    rv = None
    try:
        rv = int(s)
    except ValueError:
        pass
    return rv


def read_data(filename):
    linenum = 0
    v1 = None
    v2 = None
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if linenum == 0:
                v1 = str_to_int(line)
            elif linenum == 1:
                # print(line)
                # print(line.split(","))
                v2 = map(str_to_int, line.split(","))
            else:
                print("extra line ", linenum)
            linenum = linenum + 1
    return (v1, v2)


def part1(earliest, buses):
    print(earliest, buses)
    print("Dropping unavailable buses")
    buses = filter(None, buses)
    print("Buses ", buses)
    mingap = 100000000
    minbus = -1
    for i in buses:
        print(i)
        val = earliest // i
        sched = (val+1)*i
        gap = sched - earliest
        print((val+1)*i, earliest)
        if gap < mingap:
            mingap = gap
            minbus = i
    print(mingap, minbus, mingap*minbus)


def part2(buses):
    data = [v for v in filter(lambda v: v[1], enumerate(buses))]
    maxv = data[0]
    lcm = 1
    for v in data:
        lcm = lcm * v[1]
        if v[1] > maxv[1]:
            maxv = v
    print(data)
    print("max = ", maxv, "lcm ", lcm)

    timestamp = maxv[1]-maxv[0]
    incr = maxv[1]
    print("timestamp = ", timestamp, "increment = ", incr)
    iter = 0
    try:
        while True:
            alltrue = True
            for v in data:
                if v[1] == None:
                    continue
                if (timestamp + v[0]) % v[1] != 0:
                    alltrue = False
                    break
            if alltrue:
                print(data)
                print("Timestamp is ", timestamp, " at iter = ", iter)
                break
            timestamp = timestamp + incr
            iter = iter + 1
    except:
        print(timestamp)


def find_multiple_for_mod(n, num, m):
    q = 1
    while True:
        if (n*q % num) == m:
            return q
        q = q + 1
    return -1


def part3(buses):
    data = [v for v in filter(lambda v: v[1], enumerate(buses))]
    data = map(
        lambda v: ((v[1]-v[0]) % v[1], v[1]),
        data
    )
    parts = [1 for i in range(len(data))]
    for i in range(len(data)):
        for j in range(len(parts)):
            if j != i:
                parts[j] = parts[j] * data[i][1]
    print("parts = ", parts)
    for i in range(len(parts)):
        print("Finding remainder ", data[i][0],
              " for ", data[i][1], " for ", parts[i], " current ", parts[i] % data[i][1])
        q = find_multiple_for_mod(parts[i], data[i][1], data[i][0])
        parts[i] = parts[i]*q
    print(parts)
    sum = reduce(lambda a, b: a+b, parts)
    print(sum)
    gcd = 1
    for v in data:
        gcd = gcd * v[1]
    print(gcd)
    while sum > gcd:
        sum = sum - gcd
    print("answer ", sum)
    # while True:
    #     if (17 * 13 * q) % 19 == 3:
    #         break
    #     q = q+1


def main():
    (earliest, buses) = read_data("input.txt")
    # part1(earliest, buses)
    part3(buses)


if __name__ == "__main__":
    main()
