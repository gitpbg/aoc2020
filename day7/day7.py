
class Bag:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, count, bag):
        self.children.append((count, bag))

    def has_children(self):
        return len(self.children) != 0

    def __str__(self):
        return "Bag " + self.name + " Children " + str(self.children)

    def __repr__(self):
        return self.__str__()


def print_bag_tree(bag, depth):
    if depth > 10:
        print("TOO DEEP")
        return
    print("*" * depth + bag.name)
    for child in bag.children:
        print_bag_tree(child[1], depth+1)


def contains_bag(bag, name):
    for (bc, child) in bag.children:
        if child.name == name:
            return True
        else:
            if contains_bag(child, name):
                return True
    return False


def count_descendants(bag):
    result = 0
    for (ct, child) in bag.children:
        result = result + ct + ct * count_descendants(child)
    return result


ALLBAGS = {}


def find_or_add_bag(name):
    global ALLBAGS
    if name not in ALLBAGS:
        ALLBAGS[name] = Bag(name)
    return ALLBAGS[name]


def main():
    global ALLBAGS
    count = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            parts = line.split()
            bagcolor = parts[0].strip() + " " + parts[1].strip()
            # skip 3
            bag = find_or_add_bag(bagcolor)
            for j in range(4, len(parts), 4):
                number = parts[j]
                bagcolor = parts[j+1].strip() + " " + parts[j+2].strip()
                if number != "no":
                    child = find_or_add_bag(bagcolor)
                    bag.add_child(int(number), child)
            count = count + 1
    print(len(ALLBAGS.keys()))
    # print(ALLBAGS)
    # for (k, v) in ALLBAGS.items():

    #     if not v.has_children():
    #         print(v)
    #print_bag_tree(ALLBAGS["shiny gold"], 0)
    count = 0
    bagname = "shiny gold"
    for name, bag in ALLBAGS.items():
        if contains_bag(bag, bagname):
            count = count + 1
    print(count, " bags contain " + bagname)

    print("part 2")
    print(count_descendants(ALLBAGS["shiny gold"]))


if __name__ == "__main__":
    main()
