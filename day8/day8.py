NOP = 1
ACC = 2
JMP = 3
instructions = {
    "nop": NOP,
    "acc": ACC,
    "jmp": JMP
}


def loadfile(filename):
    global instructions
    program = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            parts = line.split()
            optxt = parts[0].strip()
            if optxt in instructions:
                opcode = instructions[optxt]
                data = int(parts[1])
                program.append((opcode, data))
    f.close()
    return program


def run(program, nopflip):
    accumulator = 0
    pc = 0
    visited = {}
    order = []
    jmpcnt = 0
    while True:
        if pc in visited:
            print("Loop detected, exiting....")
            return (0, accumulator)
        if pc >= len(program):
            print("program ended")
            return (1, accumulator)
        (op, data) = program[pc]
        visited[pc] = True
        order.append(pc)
        if op == NOP:
            pc = pc+1
        elif op == ACC:
            accumulator = accumulator + data
            pc = pc+1
        elif op == JMP:
            if pc == nopflip:
                print("jump ", pc, " converted to NOP")
                pc = pc + 1
            else:
                pc = pc + data
                jmpcnt = jmpcnt + 1

    # print(accumulator)
    # print(order)


def main():
    program = loadfile("input.txt")
    pos = 0
    while True:
        while program[pos][0] != JMP:
            pos = pos+1
        print("Jump found at ", pos)
        (ended, accumulator) = run(program, pos)
        if ended:
            print("Whew... found it. ", accumulator)
            break
        else:
            pos = pos+1
    # print(program)


if __name__ == "__main__":
    main()
