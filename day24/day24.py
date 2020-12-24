import numpy as np
# grid is in y, x format
valid_dir = ["e", "w", "se", "ne", "sw", "nw"]

hexmap_odd = {
    "e": (0, 1),
    "w": (0, -1),
    "se": (1, 1),
    "ne": (-1, 1),
    "sw": (1, 0),
    "nw": (-1, 0)
}

hexmap_even = {
    "e": (0, 1),
    "w": (0, -1),
    "se": (1, 0),
    "ne": (-1, 0),
    "sw": (1, -1),
    "nw": (-1, -1)
}

offsets = [
    hexmap_even,
    hexmap_odd
]


def readdata(filename):
    directions = []
    DEBUG = False
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            ll = len(line)
            idx = 0
            s = ""
            ldata = []
            while idx < ll:
                s = s + line[idx]
                if s in valid_dir:
                    if DEBUG:
                        print(s, " ", end="")
                    ldata.append(s)
                    s = ""
                idx = idx + 1
            if DEBUG:
                print("")
            directions.append(ldata)
    return directions

#   0  1  2  3  4  5
# 0 x x x x x x
# 1  x x x x x x
# 2 x x x x x x
# 3  x x x x x x
# 4 x x x x x x
# 5


def get_neighbor_count(grid, y, x):
    maxy, maxx = grid.shape
    curoff = offsets[y % 2]
    count = 0
    for dy, dx in curoff.values():
        nx = x + dx
        ny = y + dy
        if nx > 0 and ny > 0 and nx < maxx and ny < maxy:
            count = count + grid[ny][nx]
        else:
            print("Bounds reached")
    return count


def compute_day(tiles):
    maxy, maxx = tiles.shape
    changes = []
    for y in range(maxy):
        for x in range(maxx):
            n = get_neighbor_count(tiles, y, x)
            if tiles[y][x] == 1:
                if n == 0 or n > 2:
                    changes.append((y, x))
            elif tiles[y][x] == 0:
                if n == 2:
                    changes.append((y, x))
    for y, x in changes:
        if tiles[y][x] == 1:
            tiles[y][x] = 0
        else:
            tiles[y][x] = 1


def main():
    directions = readdata("input.txt")
    # print(directions)
    tiles = np.zeros(shape=(201, 201), dtype=int)
    reference = (100, 100)
    DEBUG = False
    miny, minx = 99999999, 99999999
    maxy, maxx = -minx, -miny
    for direction in directions:
        cury, curx = reference
        for step in direction:
            curoff = offsets[cury % 2]
            oy, ox = curoff[step]
            curx = curx + ox
            cury = cury + oy
            if curx < minx:
                minx = curx
            if cury < miny:
                miny = cury
            if curx > maxx:
                maxx = curx
            if cury > maxy:
                maxy = cury
            if DEBUG:
                print(step, cury, curx)
        if DEBUG:
            print("reached ", cury, curx, tiles[cury][curx])
        if tiles[cury][curx] == 0:
            tiles[cury][curx] = 1
        else:
            tiles[cury][curx] = 0
        if DEBUG:
            print("done ", cury, curx, tiles[cury][curx])

    print("Bounds Min x,y ", minx, miny, "Max x y", maxx, maxy)
    print(np.count_nonzero(tiles == 1))
    for day in range(0, 101):
        print(day, np.count_nonzero(tiles == 1))
        compute_day(tiles)


if __name__ == "__main__":
    main()
