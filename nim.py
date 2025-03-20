import random

class Nim():
    def __init__(self, init=[1, 3, 5, 7]):
        self.piles = init.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def avail_acts(cls, piles):
        return {(i, j) for i, pile in enumerate(piles) 
                for j in range(1, pile + 1)}

    @classmethod
    def other_plyr(cls, plyr):
        return 0 if plyr == 1 else 1

    def move(self, act):
        pile, cnt = act

        if self.winner is not None:
            raise Exception("Game already over!")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile!")
        elif cnt < 1 or cnt > self.piles[pile]:
            raise Exception("Invalid number of objects!")

        self.piles[pile] -= cnt
        self.player = Nim.other_plyr(self.player)

        if all(p == 0 for p in self.piles):
            self.winner = self.player
