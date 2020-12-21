class Expr:
    def __init__(self, value):
        self.value = value
        self.children = [None, None]

    def add_child(self, value):
        self.value

    def eval(self):
        if isinstance(self.value, (type(10),)):
            return self.value
        else:
            if isinstance(self.value, (type(""))):
                op = self.value
                if op == '+':
                    return (self.children[0].eval() + self.children[1].eval())
                elif op == "-":
                    return (self.children[0].eval() - self.children[1].eval())
                elif op == "*":
                    return (self.children[0].eval() * self.children[1].eval())


def getexpr1(s):
    ops = []
    number = ""
    curop = ""
    nesting = 0
    subexpr = ""
    for i, ch in enumerate(s):
        if ch == "(":
            nesting = nesting+1
            if nesting > 1:
                subexpr = subexpr + ch
            continue
        if ch == ")":
            nesting = nesting - 1
            if nesting == 0:
                ops.append(("expr", subexpr))
                subexpr = ""
                continue
        if nesting > 0:
            subexpr = subexpr + ch
            continue
        if ch.isdigit():
            number = number + ch
        if ch in "*+-":
            if number != "":
                ops.append(("number", int(number)))
                number = ""
            if curop != "":
                ops.append(("op", curop))
            curop = ch
    if number != "":
        ops.append(("number", int(number)))
    ops.append(("op", curop))
    print(ops)
    l = None
    r = None

    for (t, op) in ops:
        if t == "op":
            tmp = Expr(op)
            tmp.children[0] = l
            tmp.children[1] = r
            l = tmp
            r = None
        else:
            if l is None:
                if t == "number":
                    l = Expr(op)
                else:
                    l = getexpr1(op)
            elif r is None:
                if t == "number":
                    r = Expr(op)
                else:
                    r = getexpr1(op)
            else:
                print("ERROR")
                break
    return l


def part1():
    tests = [
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("2 * 3 + (4 * 5)", 26),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632)
    ]
    for (s, res) in tests:
        e = getexpr1(s)
        print(s, "Expected result", res)
        rv = e.eval()
        if rv == res:
            print("PASSED")
        else:
            print("FAILED ", rv)

    sum = 0
    debug = 1
    with open("input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            e = getexpr1(line)
            sum = sum + e.eval()
    print(sum)

# stmt = expr + expr
# expr = number OR (expr)
# f


def getexpr2(s):
    ops = []
    number = ""
    curop = ""
    nesting = 0
    subexpr = ""
    for i, ch in enumerate(s):
        if ch == "(":
            nesting = nesting+1
            if nesting > 1:
                subexpr = subexpr + ch
            continue
        if ch == ")":
            nesting = nesting - 1
            if nesting == 0:
                ops.append(("expr", subexpr))
                subexpr = ""
                continue
        if nesting > 0:
            subexpr = subexpr + ch
            continue
        if ch.isdigit():
            number = number + ch
        if ch in "*+-":
            if number != "":
                ops.append(("number", int(number)))
                number = ""
            ops.append(("op", ch))
            curop = None
    #ops.append(("op", curop))
    if number != "":
        ops.append(("number", int(number)))
    print(ops)

    l = None
    r = None

    for (t, op) in ops:
        if t == "op":
            tmp = Expr(op)
            tmp.children[0] = l
            tmp.children[1] = r
        else:
            if l is None:
                if t == "number":
                    l = Expr(op)
                else:
                    l = getexpr1(op)
            elif r is None:
                if t == "number":
                    r = Expr(op)
                else:
                    r = getexpr1(op)
            else:
                print("ERROR")
                break
    return l


def print_eval(e, depth):
    if e is None:
        return
    offset = "  " * depth
    print(offset + str(e.value))
    print_eval(e.children[0], depth+1)
    print_eval(e.children[1], depth+1)


#
# https://en.wikipedia.org/wiki/Operator-precedence_parser
#
# The Fortran I compiler would expand each operator with a sequence of parentheses. In a simplified form of the algorithm, it would

# replace + and – with ))+(( and ))-((, respectively;
# replace * and / with )*( and )/(, respectively;
# add (( at the beginning of each expression and after each left parenthesis in the original expression; and
# add )) at the end of the expression and before each right parenthesis in the original expression.
# Although not obvious, the algorithm was correct, and, in the words of Knuth, “The resulting formula is properly parenthesized, believe it or not.”[8]

# I finally gave up, added the parenthesis and deferred the parsing to the Python interpreter :-)
#
def new_eval(s):
    s = "((" + s + "))"
    s = s.replace("+", ") + (")
    s = s.replace("*", ")) * ((")
    print(s)
    return eval(s)


def part2():
    tests = [
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("1 + 2 * 3 + 4 * 5 + 6", 231),
        ("2 * 3 + (4 * 5)", 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340)
    ]
    for (s, res) in tests:
        rv = new_eval(s)
        if rv == res:
            print("PASSED")
        else:
            print("FAILED Expected ", res, " Got ", rv)
    debug = 0
    if debug == 1:
        return
    sum = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            sum = sum + new_eval(line)
    print(sum)


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()
