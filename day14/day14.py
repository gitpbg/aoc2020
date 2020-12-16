from functools import reduce


def memwrite(mem, ormask, andmask, addr, value):
    print(value, " written as ", ((value | ormask) & andmask))
    mem[addr] = ((value | ormask) & andmask)


def get_or_mask(mask):
    value = 0
    bitpos = 35
    for ch in mask:
        if ch == '1':
            value = value | 1 << bitpos
        bitpos = bitpos - 1
    return value


def get_and_mask(mask):
    value = 0
    bitpos = 35
    for ch in mask:
        if ch == '0':
            pass
        else:
            value = value | 1 << bitpos
        bitpos = bitpos - 1
    return value


def part1():
    ormask = 0
    andmask = 0
    curmask = "X"*36
    mem = {}
    with open("input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line[0:4] == "mask":
                parts = line.split()
                curmask = parts[2]
                print("mask changed to ", curmask)
                ormask = get_or_mask(curmask)
                andmask = get_and_mask(curmask)
                print("%s => OR %08x AND %08x" % (curmask, ormask, andmask))
            elif line[0:3] == "mem":
                ob = line.find('[')
                cb = line.find(']')
                es = line.find("=")

                print("mem ", line[ob+1:cb], line[es+2:])
                memwrite(mem, ormask, andmask, int(
                    line[ob+1:cb]), int(line[es+2:]))
    print(reduce(lambda a, b: a+b, mem.values()))

# what I do here is
# first scan the mask to get the positions of the X's AND to build a format string
# the pow(2, Number Of X's) is the number of addresses
# iterate over the number of address
# now the bit that are set in the iterator variable (j) are collected into an array
# these bits are then converted to a tuple and applied to the format string
# use int to convert the bitstring to a number and yield it.


def get_variations(numstr: str):
    positions = []
    pos = 35
    numtemp = ""
    for ch in numstr:
        if ch == 'X':
            positions.append(pos)
            numtemp = numtemp+"%d"
        else:
            numtemp = numtemp + ch
        pos = pos-1
#    print(numtemp)
    numaddr = 1 << (len(positions))
    for j in range(numaddr):
        bits = list(map(lambda x: 0, positions))
        for k in range(len(positions)):
            if j & (1 << k):
                bits[k] = 1
        numstr = numtemp % tuple(bits)
        yield (int(numstr, 2))


def part2():
    curmask = "X"*36
    mem = {}
    with open("input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line[0:4] == "mask":
                parts = line.split()
                curmask = parts[2]
                #print("mask changed to ", curmask, len(curmask))
            elif line[0:3] == "mem":
                ob = line.find('[')
                cb = line.find(']')
                es = line.find("=")
                addr = int(line[ob+1:cb])
                val = int(line[es+2:])
#                print("addr = ", addr, val)
                addrstr = "{:036b}".format(addr)
                result = ""
                # zip up the mask and the address string and apply the rules to get a number with X's
                for ch in zip(curmask, addrstr):
                    # print(ch)
                    if ch[0] == 'X' or ch[0] == '1':
                        result = result+ch[0]
                    else:
                        result = result+ch[1]
                # pass the string with X's to the combinatorial iterator to get the values
                for num in get_variations(result):
                    # print(num)
                    mem[num] = val
    sum = reduce(lambda a, b: a+b, mem.values())
    print("Answer is {}".format(sum))


def main():

    # set bit 2
    #    a = 10
    #    a = a | 0x2
    #    print("{:08b}".format(a))
    #    print("{:b}".format(0xff ^ 0x2))
    #    a = a & (0xff ^ 0x2)
    #    print("{:08b}".format(a))
    # clear bit 2
    # part1()
    part2()


if __name__ == "__main__":
    main()
