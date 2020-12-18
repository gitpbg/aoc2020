class Game:
    def __init__(self, numbers):
        self.history = {}
        self.last_spoken = 0
        self.turn = 1
        for n in numbers:
            self.last_spoken = n
            self.history[n] = (self.turn, -1)
            # print("Turn {} Number {}".format(self.turn, n))
            self.turn = self.turn + 1
        self.next = 0

    def next_number(self):
        next = -1
        # print("Last Spoken = {}".format(self.last_spoken))
        if self.last_spoken not in self.history:
            # print("returning 0")
            next = 0
        else:
            (last, prev) = self.history[self.last_spoken]
            if prev == -1:
                # print("{} {} was the first ever time it was spoken".format(
                #     self.last_spoken, last))
                next = 0
            else:
                # print("{} has been said before at {} and {}".format(
                #     self.last_spoken, last, prev))
                next = last - prev
        return next

    def update(self, num):
        if num in self.history:
            (last, prev) = self.history[num]
            self.history[num] = (self.turn, last)
        else:
            self.history[num] = (self.turn, -1)

    def run(self, ending):
        while self.turn <= ending:
            n = self.next_number()
            if self.turn == ending:
                print("Turn {} Number {}".format(self.turn, n))
            self.update(n)
            self.last_spoken = n
            self.turn = self.turn + 1


def main():
    id = 7
    input = [
        [0, 3, 6],
        [1, 3, 2],
        [2, 1, 3],
        [1, 2, 3],
        [2, 3, 1],
        [3, 2, 1],
        [3, 1, 2],
        [8, 13, 1, 0, 18, 9],
    ]
    g = Game(input[id])
    # g.run(2020)
    g.run(30000000)


if __name__ == "__main__":
    main()
