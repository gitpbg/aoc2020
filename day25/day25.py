import sys


def figure_loop_size(subject, pkey):
    v = 1
    ls = 0
    while v != pkey:
        v = (v * subject) % 20201227
        # print(v)
        ls = ls + 1
        if ls > 100000000:
            print("too many iterations")
            sys.exit(1)
    return ls


def transform(number, loopsize):
    v = 1
    debug = (loopsize < 10)

    for _ in range(loopsize):
        v = (v * number) % 20201227
    return v


def main():
    testdata = [5764801, 17807724]
    realdata = [2069194, 16426071]
#    (v1 ** ls2) mod 20201226 = (v2 ** ls1) mod 20201226

    data = realdata
    loop_sizes = list(map(lambda x: figure_loop_size(7, x), data))
    print(loop_sizes)
    print(transform(data[0], loop_sizes[1]))
    print(transform(data[1], loop_sizes[0]))
    pass


if __name__ == "__main__":
    main()
