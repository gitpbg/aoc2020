filename = "input1.txt"
data = []
with open(filename) as f:
    for line in f.readlines():
        data.append(int(line))
    f.close()

print(len(data))
done = 0
for i in range(0, len(data)):
    for j in range(i+1, len(data)):
        for k in range(i+2, len(data)):
            if data[i]+data[j]+data[k] == 2020:
                print(i, j, k, data[i], data[j],
                      data[k], data[i]*data[j]*data[k])
                done = 1
                break  # k loop
        if done == 1:
            break  # j loop
    if done == 1:
        break  # i loop
