import sys
import numpy as np


def readdata(filename):
    data = []
    allsep = "(contains "
    aslen = len(allsep)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            pos = line.find(allsep)
            ingredients = line[:pos].strip().split()
            allergens = line[pos+aslen:-1].split(", ")
            data.append((ingredients, allergens))
    return data


def make_sets(data):
    ingrs = set()
    agens = set()
    for item, agen in data:
        for ingr in item:
            ingrs.add(ingr)
        for a in agen:
            agens.add(a)
    return ingrs, agens


def make_ingr_allergen_array(data, ingredients, allergens):
    arr = np.zeros((len(allergens), len(ingredients)), dtype=int)
    ingredients_index = {}
    allergen_index = {}
    for i, item in enumerate(ingredients):
        ingredients_index[item] = i
    for i, agen in enumerate(allergens):
        allergen_index[agen] = i

    for item, agens in data:
        for ingr in item:
            col = ingredients_index[ingr]
            for agen in agens:
                row = allergen_index[agen]
                arr[row][col] = arr[row][col] + 1

    return arr


def print_array(arr, items, allergens):
    for (r, a) in enumerate(allergens):
        if r == 0:
            print("{:8s}".format(" "), end="")
            for i in items:
                print("{:8s} ".format(i), end="")
            print("")
        print("{:8s}".format(a), end="")
        for (c, i) in enumerate(items):
            print("{:8d}".format(arr[r][c]), end="")
        print("")


def find_unique_max(arr, identified_item, identified_allergen):
    rv = []
    overall_max = -1
    overall_max_row = -1
    rows, cols = arr.shape

    for r in range(rows):
        if r in identified_allergen:
            continue
        rmax = -1
        rmax_first_index = -1
        rmax_count = 0
        for c in range(cols):
            if c in identified_item:
                continue
            v = arr[r][c]
            if v == rmax:
                rmax_count = rmax_count + 1
            if v > rmax:
                rmax = v
                rmax_first_index = c
                rmax_count = 1
        if rmax_count == 1:
            print("row ", r, " has a unique max ", rmax)
            rv.append((r, rmax_first_index))
        if rmax > overall_max:
            overall_max = rmax
            overall_max_row = r
    print("overall max row = ", overall_max_row)
    return rv, overall_max_row


def main():
    data = readdata("input.txt")
    ingrs, agens = make_sets(data)
    # convert to lists for easy indexing
    ingredients = list(ingrs)
    allergens = list(agens)
    ingredients.sort()
    allergens.sort()
    arr = make_ingr_allergen_array(data, ingredients, allergens)
    print_array(arr, ingredients, allergens)
    added = True
    identified_allergen = {}
    identified_item = {}
    while added:
        added = False
        (umrows, maxrow) = find_unique_max(
            arr, identified_item, identified_allergen)
        print(umrows, maxrow)
        for r, c in umrows:
            print("Row ", r, " for ",
                  allergens[r], "has a unique max at column ", c, ingredients[c])
            identified_allergen[r] = c
            identified_item[c] = r
            added = True
        print("Row ", maxrow, " for ", allergens[maxrow], "has the most items")
    print(len(allergens), " and ", len(identified_allergen))
    print(len(ingredients), " items and ", len(identified_item), " identified")
    identified_names = {}
    dangerous = []
    for i in identified_item.keys():
        print("item ", ingredients[i])
        aindex = identified_item[i]
        allergen = allergens[aindex]
        dangerous.append((ingredients[i], allergen))
        identified_names[ingredients[i]] = True
    count = 0
    for item, agens in data:
        for ingr in item:
            if ingr not in identified_names:
                count = count + 1

    print("Count = ", count)
    print(dangerous)
    dangerous.sort(key=lambda x: x[1])
    print(dangerous)
    print(",".join([d[0] for d in dangerous]))


if __name__ == "__main__":
    main()
