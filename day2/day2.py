def process_password(line):
    line = line.strip()
    parts = line.split(" ")
    minmax = parts[0].split("-")
    themin = int(minmax[0])
    themax = int(minmax[1])
    thechar = parts[1][0]
    passwd = parts[2]
    count = 0
    for i in range(0, len(passwd)):
        if passwd[i] == thechar:
            count = count + 1
    if count >= themin and count <= themax:
        return True
    return False


def process_password2(line):
    line = line.strip()
    parts = line.split(" ")
    minmax = parts[0].split("-")
    themin = int(minmax[0])-1
    themax = int(minmax[1])-1
    thechar = parts[1][0]
    passwd = parts[2]
    a = passwd[themin] == thechar
    b = passwd[themax] == thechar
    return (a and not b) or (not a and b)


filename = "input.txt"
count = 0
with open(filename, "r") as f:
    for line in f.readlines():
        result = process_password2(line)
        if result:
            count = count + 1

print(count)
