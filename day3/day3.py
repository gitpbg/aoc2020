def loaddata(filename):
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            data.append(line.strip())
        f.close()
    return data


def findtrees(data, startx, starty, diffx, diffy):
    pos_x = startx
    pos_y = starty
    num = 0
    rows = len(data)
    columns = len(data[0])
    while pos_y < rows:
        cur_row = data[pos_y]
        if cur_row[pos_x % columns] == '#':
            num = num + 1
        pos_x = pos_x + diffx
        pos_y = pos_y + diffy
    return num


def main():
    data = loaddata("input.txt")
    print(len(data), " rows", len(data[0]), " columns")
    # print(data)
    answer = 1
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    for (diffx, diffy) in slopes:
        num = findtrees(data, 0, 0, diffx, diffy)
        print(num, " trees for %d, %d" % (diffx, diffy))
        answer = answer * num
    print("The answer is ", answer)


if __name__ == "__main__":
    main()
