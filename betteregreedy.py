import random
from functools import reduce
from nim import Nim

class GrundyNim():
    def __init__(self, alpha=0.5):
        self.Q = dict()
        self.N = dict()
        self.alpha = alpha
        self.epsilon = 1.0
        self.k = 1
        self.initnimber()
    
    def nimsum(self, heaps):
        return reduce(lambda x, y: x ^ y, heaps, 0)

    def initnimber(self):
        maxheap = 8
        num_heaps = 4
        heap_sizes = [maxheap] * num_heaps

        def generate_heaps(current_heaps, depth):
            if depth == num_heaps:
                s = tuple(current_heaps)
                nimSum = self.nimsum(s)
                if nimSum == 0:
                    for a in Nim.avail_acts(s):
                        heap, count = a
                        newheaps = list(s)
                        newheaps[heap] -= count
                        newNimSum = self.nimsum(newheaps)
                        if newNimSum == 0:
                            self.Q[(s, a)] = 0.5
                            self.N[(s, a)] = 5
                        else:
                            self.Q[(s, a)] = -0.5
                            self.N[(s, a)] = 3
                else:
                    for a in Nim.avail_acts(s):
                        heap, count = a
                        newheaps = list(s)
                        newheaps[heap] -= count
                        newNimSum = self.nimsum(newheaps)
                        if newNimSum == 0:
                            self.Q[(s, a)] = 0.8
                            self.N[(s, a)] = 5
                        else:
                            self.Q[(s, a)] = -0.2
                            self.N[(s, a)] = 3
            else:
                for i in range(1, heap_sizes[depth] + 1):
                    generate_heaps(current_heaps + [i], depth + 1)

        generate_heaps([], 0)
    
    def pi_s(self, s):
        A = list(Nim.avail_acts(s))
        if random.random() < self.epsilon:
            return random.choice(A)
        return max(A, key=lambda a: self.Q.get((tuple(s), a), 0), default=None)
    
    def MCPolicyEval(self, episode):
        S, A, R = zip(*episode)
        T = len(S) - 1
        G = 0
        for t in range(T-1, -1, -1):
            s = S[t]
            a = A[t]
            r = R[t]
            G = r + self.alpha * G
            SApair = (tuple(s), a)
            self.N[SApair] = self.N.get(SApair, 0) + 1
            self.Q[SApair] = self.Q.get(SApair, 0) + (1.0/self.N[SApair]) * (G - self.Q.get(SApair, 0))
        self.k += 1
        self.epsilon = 1.0/self.k
