from functools import reduce


class DimIterator:
    def __init__(self, pfrom, pto, exclude=None):
        self.pfrom = pfrom
        self.pto = pto
        self.exclude = exclude
        self.counter = list(pfrom)
        self.done = False

    def __iter__(self):
        while not self.done:
            if not self.done:
                yield(tuple(self.counter))
                self.done = tuple(self.counter) == self.pto
            while(True):
                carry = 1
                for index in range(len(self.counter)):
                    self.counter[index] = self.counter[index] + carry
                    if self.counter[index] > self.pto[index]:
                        self.counter[index] = self.pfrom[index]
                    else:
                        break
                if self.exclude is not None:
                    if self.exclude == tuple(self.counter):
                        if self.exclude == self.pto:
                            self.done = True
                            break
                        else:
                            continue
                    else:
                        break
                else:
                    break


class Dimensions:
    def __init__(self, ndims):
        self.dims = [[0, 0] for i in range(ndims)]
        # print(self.dims)

    def update_dimensions(self, c):
        for i in range(len(self.dims)):
            if c[i] < self.dims[i][0]:
                self.dims[i][0] = c[i]
            if c[i] > self.dims[i][1]:
                self.dims[i][1] = c[i]

    def neighbors(self, c):
        pfrom = tuple([t - 1 for t in c])
        pto = tuple([t+1 for t in c])
        return DimIterator(pfrom, pto, c)

    def allpoints(self):
        pfrom = tuple([self.dims[i][0]-1 for i in range(len(self.dims))])
        pto = tuple([self.dims[i][1]+1 for i in range(len(self.dims))])
        return DimIterator(pfrom, pto)


class Conway:
    def __init__(self, ndims):
        self.cells = {}
        self.activations = []
        self.deactivations = []
        self.dims = Dimensions(ndims)

    def update_bounds(self, c):
        self.dims.update_dimensions(c)

    def activate(self, c):
        if c in self.cells:
            return
        self.update_bounds(c)
        self.activations.append(c)

    def deactivate(self, c):
        if c in self.cells:
            self.deactivations.append(c)

    def count_neighbors(self, c):
        count = 0
        for n in self.dims.neighbors(c):
            if n in self.cells:
                count = count + 1
        return count

    def is_active(self, c):
        return c in self.cells

    def apply(self):
        # print(self.deactivations)
        for c in self.deactivations:
            del self.cells[c]
        # print(self.activations)
        for c in self.activations:
            self.cells[c] = True
        self.deactivations = []
        self.activations = []

    def readfile(self, filename):
        with open(filename, "r") as f:
            for row, line in enumerate(f.readlines()):
                line = line.strip()
                for pos, ch in enumerate(line):
                    if ch == '#':
                        if len(self.dims.dims) == 3:
                            self.activate((pos, row, 0))
                        else:
                            self.activate((pos, row, 0, 0))
            # print("x = ", linelen, "y = ", numlines)
        self.apply()

    def step(self):
        for c in self.dims.allpoints():
            num = self.count_neighbors(c)
            if self.is_active(c):
                if (num == 2 or num == 3):
                    pass
                else:
                    self.deactivate(c)
            else:
                if num == 3:
                    self.activate(c)
        self.apply()

    def count_active(self):
        return len(self.cells)


def main():
    part = 1
    dims = 3
    if part == 1:
        dims = 3
    elif part == 2:
        dims = 4
    else:
        print("illegal part")
        return
    c = Conway(dims)
    c.readfile("test.txt")
    for i in range(6):
        print("Step ", i)
        c.step()
    print("Active Cells = ", c.count_active())


if __name__ == "__main__":
    main()
