
def get_row_and_seat(bcode):
    row = 0
    seat = 0
    for i in bcode[0:7]:
        row = row * 2
        if i == 'B':
            row = row + 1
    for i in bcode[7:]:
        seat = seat * 2
        if i == 'R':
            seat = seat+1

    return (row, seat)


def main():
    highest = 0
    #testdata = ["FBFBBFFRLR", "BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"]
    f = open("input.txt", "r")
    ids = []
    for teststr in f.readlines():
        teststr = teststr.strip()
        (row, seat) = get_row_and_seat(teststr)
        id = row * 8 + seat
        ids.append(id)
        if id > highest:
            highest = id
    print("highest = ", highest)
    ids.sort()
    # print(ids)
    for i in range(0, len(ids)-1):
        if ids[i]+1 != ids[i+1]:
            print(ids[i]+1)


if __name__ == "__main__":
    main()
