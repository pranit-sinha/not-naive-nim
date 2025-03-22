import random
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
        return heaps[0] ^ heaps[1] ^ heaps[2] ^ (heaps[3] if len(heaps) > 3 else 0)
    
    def initnimber(self):
        maxheap = 20
        
        for i in range(1, maxheap+1):
            for j in range(1, maxheap+1):
                for k in range(1, maxheap+1):
                    s = (i, j, k)
                    nimSum = self.nimsum(s)
                    
                    if nimSum == 0:  
                        for a in Nim.avail_acts(s):
                            self.Q[(s, a)] = -0.5
                            self.N[(s, a)] = 5
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
