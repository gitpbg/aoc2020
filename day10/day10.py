
def read_data(filename):
    rv = [0]
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            rv.append(int(line))
    return rv


count = 0


# def find_next(data, pos):
#     global count
#     if pos == len(data)-1:
#         count = count + 1
#         if (count % 100000) == 0:
#             print(count, end=" ", flush=True)
#     cur = data[pos]
#     choice = 0
#     # print("starting from %d value %d" % (pos, cur))
#     for i in range(pos+1, len(data)):
#         if data[i]-cur <= 3:
#             # print("choice %d at %d" % (data[i], i))
#             choice = choice + 1
#             find_next(data, i)


def main():
    data = read_data("input.txt")
    data.sort()
    print(data)
    data.append(data[-1]+3)
    max = data[-1]
    print(data[-1])
    num_one = 0
    num_three = 0
    for i in range(len(data)-1):
        diff = data[i+1]-data[i]
        if diff == 3:
            num_three = num_three + 1
        elif diff == 1:
            num_one = num_one + 1
    print("ones " + str(num_one), " threes " + str(num_three))
    print("Answer is " + str(num_one*num_three))
    paths = {}
    paths[0] = 1
    for i in range(len(data)):
        cur = data[i]
        for j in range(1, 4):
            next = cur + j
            if next in data:
                if next in paths:
                    paths[next] = paths[next] + paths[cur]
                    print("adding %d paths to adapter %d" % (paths[cur], next))
                else:
                    paths[next] = paths[cur]

    print(paths[max])


if __name__ == "__main__":
    main()
