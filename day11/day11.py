FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'
OOB = '@'


def read_data(filename):
    rv = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                return rv
            row = []
            for ch in line:
                row.append(ch)
            rv.append(row)
    f.close()
    return rv


def makearray(rows, columns):
    return [[FLOOR for j in range(columns)] for i in range(rows)]


def copy(src, dest):
    (rows, cols) = (len(src), len(src[0]))
    for i in range(rows):
        for j in range(cols):
            dest[i][j] = src[i][j]


neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0),
             (1, 0), (-1, 1), (0, 1), (1, 1)]


def calculate_next1(src, dest):
    global neighbors
    numchanged = 0
    (rows, cols) = (len(src), len(src[0]))
    for row in range(rows):
        for col in range(cols):
            nbrcount = 0
            if src[row][col] == FLOOR:
                dest[row][col] == FLOOR
                continue
            for (nx, ny) in neighbors:
                npy = row + ny
                npx = col + nx
                if npy >= 0 and npy < rows and npx >= 0 and npx < cols:
                    if src[npy][npx] == OCCUPIED:
                        nbrcount = nbrcount + 1
            if row == 0 and col == 0:
                print("neighbor count ", nbrcount)
            if nbrcount == 0 and src[row][col] == EMPTY:
                dest[row][col] = OCCUPIED
                numchanged = numchanged + 1
            elif nbrcount >= 4 and src[row][col] == OCCUPIED:
                dest[row][col] = EMPTY
                numchanged = numchanged + 1
            else:
                dest[row][col] = src[row][col]
    return numchanged


def inbounds(rows, cols, r, c):
    return c >= 0 and r >= 0 and r < rows and c < cols


def get_neighbor_state(data, cc, cr, nc, nr):
    rows = len(data)
    cols = len(data[0])
    c = cc + nc
    r = cr + nr
    rv = FLOOR
    try:
        while inbounds(rows, cols, r, c):
            if data[r][c] == OCCUPIED:
                rv = OCCUPIED
                break
            elif data[r][c] == EMPTY:
                rv = EMPTY
                break
            c = c + nc
            r = r + nr
    except IndexError:
        print("IndexError at %d %d rows = %d cols = %d" % (r, c, rows, cols))
        raise
    return rv


def calculate_next2(src, dest):
    global neighbors
    numchanged = 0
    (rows, cols) = (len(src), len(src[0]))
    for row in range(rows):
        for col in range(cols):
            nbrcount = 0
            if src[row][col] == FLOOR:
                dest[row][col] == FLOOR
                continue
            for (nx, ny) in neighbors:
                if get_neighbor_state(src, col, row, nx, ny) == OCCUPIED:
                    nbrcount = nbrcount+1
            #print(row, col, nbrcount)
            if nbrcount == 0 and src[row][col] == EMPTY:
                dest[row][col] = OCCUPIED
                numchanged = numchanged + 1
            elif nbrcount >= 5 and src[row][col] == OCCUPIED:
                dest[row][col] = EMPTY
                numchanged = numchanged + 1
            else:
                dest[row][col] = src[row][col]
    return numchanged


def print_layout(data):
    print()
    total = 0
    for row in data:
        total = total + row.count(OCCUPIED)
        print("".join(row))
    print()
    return total


def part1(data):
    (rows, columns) = (len(data), len(data[0]))
    nextstep = makearray(rows, columns)
    curstep = makearray(rows, columns)
    copy(data, curstep)
    # print_layout(data)
    # print_layout(curstep)
    iter = 0
    while True:
        numchanged = calculate_next1(curstep, nextstep)
        # print_layout(nextstep)
        if numchanged == 0:
            print("breaking at iter ", iter)
            occupied = print_layout(curstep)
            print("occupied = ", occupied)
            break
        tmp = curstep
        curstep = nextstep
        nextstep = tmp
        # print_layout(curstep)
        iter = iter + 1
        if iter > 200:
            break


def part2(data):
    (rows, columns) = (len(data), len(data[0]))
    nextstep = makearray(rows, columns)
    curstep = makearray(rows, columns)
    copy(data, curstep)
    iter = 0
    while True:
        print("Iteration %d" % (iter))
        # print_layout(curstep)
        numchanged = calculate_next2(curstep, nextstep)
        # print_layout(nextstep)
        if numchanged == 0:
            print("breaking at iter ", iter)
            occupied = print_layout(curstep)
            print("occupied = ", occupied)
            break
        tmp = curstep
        curstep = nextstep
        nextstep = tmp
        # print_layout(curstep)
        iter = iter + 1
        if iter > 200:
            break


def main():
    data = read_data('input.txt')
    # part1(data)
    part2(data)


if __name__ == "__main__":
    main()
