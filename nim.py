import random

class Nim():
    def __init__(self, init=[1, 3, 5, 7]):
        self.heaps = init.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def avail_acts(cls, heaps):
        return {(i, j) for i, heap in enumerate(heaps) 
                for j in range(1, heap + 1)}

    @classmethod
    def other_plyr(cls, plyr):
        return 0 if plyr == 1 else 1

    def move(self, act):
        heap, cnt = act

        if self.winner is not None:
            raise Exception("Game already over!")
        elif heap < 0 or heap >= len(self.heaps):
            raise Exception("Invalid heap!")
        elif cnt < 1 or cnt > self.heaps[heap]:
            raise Exception("Invalid number of objects!")

        self.heaps[heap] -= cnt
        self.player = Nim.other_plyr(self.player)

        if all(h == 0 for h in self.heaps):
            self.winner = self.player
