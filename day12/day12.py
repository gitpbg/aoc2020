
import math
vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
direction_str = "NESW"


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.orientation = 1
        self.error = None

    def turnleft(self):
        self.orientation = (self.orientation - 1 + 4) % 4

    def turnright(self):
        self.orientation = (self.orientation + 1 + 4) % 4

    def forward(self, units):
        global vectors
        self.x = self.x + vectors[self.orientation][0]*units
        self.y = self.y + vectors[self.orientation][1]*units

    def north(self, units):
        self.y = self.y + units

    def south(self, units):
        self.y = self.y - units

    def west(self, units):
        self.x = self.x - units

    def east(self, units):
        self.x = self.x + units

    def manhattan_distance(self):
        tx = self.x
        ty = self.y
        if tx < 0:
            tx = -tx
        if ty < 0:
            ty = -ty
        return tx+ty


class WayPointShip:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.wpx = 10
        self.wpy = 1
        self.wpangle = 0
        self.orientation = 1
        self.error = None

    def rotateLeft90(self):
        (self.wpx, self.wpy) = (-self.wpy, self.wpx)

    def rotateRight90(self):
        (self.wpx, self.wpy) = (self.wpy, -self.wpx)
#        return (y, -x)

    # def rotate(self, angle):
    #     angle = angle * math.pi/180.0
    #     nx = int(self.wpx * math.cos(angle) - self.wpy * math.sin(angle))
    #     ny = int(self.wpx * math.sin(angle) + self.wpy * math.cos(angle))
    #     self.wpx = nx
    #     self.wpy = ny

    def turnleft(self):
        self.rotateLeft90()
        # self.rotate(90)

    def turnright(self):
        self.rotateRight90()
#        self.rotate(-90)

    def forward(self, units):
        global vectors
        self.x = self.x + self.wpx*units
        self.y = self.y + self.wpy*units

    def north(self, units):
        self.wpy = self.wpy + units

    def south(self, units):
        self.wpy = self.wpy - units

    def west(self, units):
        self.wpx = self.wpx - units

    def east(self, units):
        self.wpx = self.wpx + units

    def manhattan_distance(self):
        print(self.x, self.y)
        tx = self.x
        ty = self.y
        if tx < 0:
            tx = -tx
        if ty < 0:
            ty = -ty
        return tx+ty


def read_file(filename):
    ship = Ship()
    ship2 = WayPointShip()
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                break
            (action, units) = (line[0], int(line[1:]))
            if action == 'N':
                ship.north(units)
                ship2.north(units)
            elif action == 'E':
                ship.east(units)
                ship2.east(units)
            elif action == 'S':
                ship.south(units)
                ship2.south(units)
            elif action == 'W':
                ship.west(units)
                ship2.west(units)
            elif action == 'L':
                while units > 0:
                    ship.turnleft()
                    ship2.turnleft()
                    units = units - 90
            elif action == 'R':
                while units > 0:
                    ship.turnright()
                    ship2.turnright()
                    units = units - 90
            elif action == 'F':
                ship.forward(units)
                ship2.forward(units)
            else:
                print("Unknown Action")
                ship.error = "Unknown Action"
                break
            print("Ship 1", action, units, ship.x, ship.y)
            print("Ship 2", action, units, ship2.x,
                  ship2.y, ship2.wpx, ship2.wpy)
    return (ship, ship2)


def main():
    (ship, ship2) = read_file("input.txt")
    if ship.error is None:
        print("Manhattan Distance = %d" % (ship.manhattan_distance()))
    if ship2.error is None:
        print("Manhattan Distance for Ship2 is %d" %
              (ship2.manhattan_distance()))


if __name__ == "__main__":
    # x = 10
    # y = 4
    # angle = -90.0*math.pi/180.0
    # nx = x * math.cos(angle) - y * math.sin(angle)
    # ny = x * math.sin(angle) + y * math.cos(angle)
    # print(nx, ny)
    # x = 1
    # y = 1
    # print("Starting Rotate Right ", x, y)
    # for i in range(4):
    #     (x, y) = rotateRight90(x, y)
    #     print(x, y)
    # x = 1
    # y = 1
    # print("Starting Rotate Left ", x, y)
    # for i in range(4):
    #     (x, y) = rotateLeft90(x, y)
    #     print(x, y)
    # print(rotateRight90(10, 4))
    main()
