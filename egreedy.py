import random
from nim import Nim

class EpsilonGreedyNim():
    def __init__(self, alpha=0.5):
        self.Q = dict()
        self.N = dict()
        self.alpha = alpha
        self.epsilon = 1.0
        self.k = 1

    def getQVal(self, s, a):
        return self.Q.get((tuple(s), a), 0)

    def bestFutureRwd(self, s):
        A = Nim.avail_acts(s)
        if not A:
            return 0
        return max((self.getQVal(s, act) for act in A), default=0)

    def chooseAct(self, s, useEpsilon=True):
        A = list(Nim.avail_acts(s))
        
        if useEpsilon and random.random() < self.epsilon:
            return random.choice(A)
        
        return max(A, key=lambda act: self.getQVal(s, act), default=None)

    def updateRule(self, episode):
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
