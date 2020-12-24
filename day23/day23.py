class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.value_map = {}

    def add_value(self, v):
        if v in self.value_map:
            assert False, "Duplicate Value {}".format(v)
        nn = Node(v)
        self.value_map[v] = nn
        self.add_node(nn)

    def add_node(self, n):
        if self.head is None:
            self.head = n
            self.tail = n
        else:
            n.prev = self.tail
            self.tail.next = n
            self.tail = n

    def find_value(self, v):
        nn = self.value_map.get(v, None)
        #assert nn is not None, "Value {} not found".format(v)
        return nn

    def remove_after(self, v):
        nn = self.find_value(v)
        if nn == self.tail:
            rv = self.head
            self.head = self.head.next
            self.head.prev = None
        else:
            rv = nn.next
            if rv == self.tail:
                self.tail = nn
                nn.next = None
            else:
                rn = rv.next
                nn.next = rn
                rn.prev = nn

        rv.prev = None
        rv.next = None
        return rv

    def insert_after(self, v, n):
        nn = self.find_value(v)
        if nn == self.tail:
            n.prev = self.tail
            self.tail.next = n
            n.next = None
            self.tail = n
        else:
            n.next = nn.next
            n.prev = nn
            n.prev.next = n
            n.next.prev = n

    def get_next(self, v):
        nn = self.find_value(v)
        if nn == self.tail:
            return self.head
        else:
            return nn.next

    def print_forward(self, prefix="", highlight=None):
        print(prefix, ":", end="")
        nn = self.head
        while nn is not None:
            if highlight is not None and nn.value == highlight:
                print("({}) ".format(nn.value), end="")
            else:
                print("{} ".format(nn.value), end="")
            nn = nn.next
        print("")

    def print_backward(self, prefix=""):
        print(prefix, ":", end="")
        nn = self.tail
        while nn is not None:
            print(nn.value, end="")
            nn = nn.prev
        print("")

    def print_from_one(self):
        one = self.find_value(1)
        n = one.next
        while n != one:
            print(n.value, end="")
            n = n.next
            if n is None:
                n = self.head


def test_circular_buffer():
    c = CircularLinkedList()
    for i in range(1, 10):
        c.add_value(i)
    c.print_forward()
    c.print_backward()
    n1 = c.remove_after(6)
    print("removed ", n1.value)
    c.print_forward()
    n2 = c.remove_after(8)
    print("removed ", n2.value)
    c.print_forward("pf")
    c.print_backward("pb")
    n3 = c.remove_after(8)
    print('removed ', n3.value)
    c.print_forward("hr")
    c.print_backward("hr")
    c.insert_after(8, n3)
    c.insert_after(8, n2)
    c.insert_after(8, n1)
    c.print_forward()
    c.print_backward()
    print(c.get_next(1).value)
    c.print_forward("test highlight", highlight=5)


def playgame(s, part, moves):
    cups = CircularLinkedList()
    maxval = -1
    numcups = 0
    for n in s:
        val = int(n)
        cups.add_value(val)
        if val > maxval:
            maxval = val
        numcups = numcups + 1
    if part == 2:
        for nextval in range(maxval+1, 1000001):
            cups.add_value(nextval)
            numcups = numcups + 1
    print("{} cups".format(numcups))
    turn = 1
    curcup = cups.head
    a = None
    b = None
    c = None
    DEBUG = False
    while turn <= moves:
        if DEBUG:
            cups.print_forward("Turn {}".format(turn), highlight=curcup.value)
        a = cups.remove_after(curcup.value)
        b = cups.remove_after(curcup.value)
        c = cups.remove_after(curcup.value)
        if DEBUG:
            print("Pickup ", a.value, b.value, c.value)
            cups.print_forward("After removal", highlight=curcup.value)
        dest = curcup.value
        while True:
            dest = dest - 1
            if dest <= 0:
                dest = numcups
            if dest == a.value or dest == b.value or dest == c.value:
                continue
            break
        if DEBUG:
            print("Dest ", dest)
        cups.insert_after(dest, c)
        cups.insert_after(dest, b)
        cups.insert_after(dest, a)
        curcup = curcup.next
        if curcup is None:
            curcup = cups.head

        if DEBUG:
            cups.print_forward("End Turn {}".format(turn),
                               highlight=curcup.value)
        turn = turn + 1
        if (turn % 100000) == 0:
            print(turn)
    if part == 1:
        cups.print_from_one()
    else:
        a = cups.get_next(1)
        b = cups.get_next(a.value)
        print(a.value, b.value, a.value*b.value)


def main():
    #s = "389125467"
    s = "215694783"
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    playgame(s, 2, 10000000)
    pr.disable()
    pr.print_stats(sort="time")
    # playgame(s, 10000000)


if __name__ == "__main__":
    # test_circular_buffer()
    main()
