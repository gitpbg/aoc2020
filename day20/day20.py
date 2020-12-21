
ORI_ROT0 = 0
ORI_ROT90 = 1
ORI_ROT180 = 2
ORI_ROT270 = 3
FLIPX_ROT0 = 4
FLIPX_ROT90 = 5
FLIPX_ROT180 = 6  # same as FLIPY
FLIPX_ROT270 = 7

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
directions = (NORTH, EAST, SOUTH, WEST)
dirnames = ("North", "East", "South", "West")


def reverse_side(side):
    tmp = list("{:010b}".format(side))
    tmp.reverse()
    return int("".join(tmp), 2)


def inverse_side(side):
    assert(0)
    return (side & 0x3FF) ^ 0x3FF


def tonumber(s, doreverse=False):
    s = s.replace("#", "1")
    s = s.replace(".", "0")
    res = int(s, 2)
    # print("{} => {}".format(s, res))
    return res


def tonumber2(s, doreverse=False):
    tmp = list(s)
    tmp.reverse()
    rvs = "".join(tmp)
    if doreverse:
        tmp2 = rvs + s
    else:
        tmp2 = s + rvs
    tmp2 = tmp2.replace("#", "1")
    tmp2 = tmp2.replace(".", "0")
    tmp2 = '1' + tmp2 + '1'
    return int(tmp2, 2)


def opposite_directon(dir):
    return (dir+2) % 4


class Tile:
    def __init__(self, tileid, top, right, bottom, left, orientation=0):
        self.id = tileid
        self.sides = (top, right, bottom, left)
        tmp = []
        for s in self.sides:
            tmp.append(s)
            tmp.append(reverse_side(s))
        self.allvalues = tuple(tmp)
        self.orientation = orientation

    def copy(self):
        t = Tile(self.id, *self.sides, self.orientation)
        return t

    def rotate(self):
        flipped = self.orientation & 0x4
        ori = self.orientation & 0x3
        self.orientation = ((ori + 1) % 4) | flipped
        res = [0 for i in range(4)]
        for i in range(4):
            j = (i+1) % 4
            if i == 0 or i == 2:
                res[j] = self.sides[i]
            else:
                # res[j] = inverse_side(self.sides[i])
                res[j] = reverse_side(self.sides[i])
        self.sides = res

    def hflip(self):
        tmp = (
            reverse_side(self.sides[0]),
            self.sides[3],
            reverse_side(self.sides[2]),
            self.sides[1]
        )
        self.sides = tmp

    def vflip(self):
        tmp = (
            self.sides[2],
            reverse_side(self.sides[1]),
            self.sides[0],
            reverse_side(self.sides[3]),
        )
        self.sides = tmp

    def __str__(self):
        return "ID:{} Orientation:{} Sides:{}".format(self.id, self.orientation, str(self.sides))


def canmatch(t1, t2, dir):
    opp = (dir+2) % 4
    return t1.sides[dir] == t2.sides[opp]


def readdata(filename):
    tiles = {}
    with open(filename, "r") as f:
        curid = -1
        curtile = []
        for line in f.readlines():
            line = line.strip()
            if line == "":
                if curid > 0:
                    left = ""
                    right = ""
                    top = ""
                    bot = ""
                    last = len(curtile)-1

                    for (i, row) in enumerate(curtile):
                        if i == 0:
                            top = row
                        if i == last:
                            bottom = row
                        left = left + row[0]
                        right = right + row[-1]
                    # print("tileid", curid)
                    tid = tonumber(top)
                    rid = tonumber(right)
                    bid = tonumber(bottom)
                    lid = tonumber(left)
                    # print(tid, bid, lid, rid)
                    t = Tile(curid, tid, rid, bid, lid)
                    tiles[curid] = t

                curid = -1
                curtile = []
                continue
            elif ":" in line:
                parts = line.split()
                if parts[0] == "Tile":
                    curid = int(parts[1][:-1])
                    # print("Tile ID=", curid)
            else:
                curtile.append(line)
    return tiles


def main():
    tiles = readdata("test.txt")
    connected = {}
    t = list(tiles.values())[0]
    connections = {}
    for t in tiles.values():
        connected[t.id] = 0
        for tt in tiles.values():
            if t.id == tt.id:
                continue
            count = 0
            key = ""
            if t.id < tt.id:
                key = "{}:{}".format(t.id, tt.id)
            else:
                key = "{}:{}".format(t.id, tt.id)
            if key in connections:
                print("Skipping ", t.id, tt.id,
                      " because they are already connected")
                continue
            s1 = set(t.allvalues)
            s2 = set(tt.allvalues)
            ixn = s1.intersection(s2)
            if len(ixn) > 0:
                connected[t.id] = connected[t.id] + 1

    ans = 1
    corners = []
    for c, v in connected.items():
        if v == 2:
            print("Tile ", c, " is a corner")
            ans = ans * tiles[c].id
            corners.append(c)
    print(ans)


if __name__ == "__main__":
    main()
