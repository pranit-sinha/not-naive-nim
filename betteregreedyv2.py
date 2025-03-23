import random
from functools import reduce
from nim import Nim

class GrundyNim():
    def __init__(self, alpha=0.5):
        self.Q = dict()
        self.N = dict()
        self.nimberMap = dict()
        self.alpha = alpha
        self.epsilon = 1.0
        self.k = 1
        self.initnimber()
    
    def nimsum(self, heaps):
        return reduce(lambda x, y: x ^ y, heaps, 0)
    
    def initnimber(self):
        maxheap = 20
        num_heaps = 4
        heap_sizes = [maxheap] * num_heaps
    
        def generate_heaps(current_heaps, depth):
            if depth == num_heaps:
                s = tuple(current_heaps)
                nimberKey = self.nimkey(s)
    
                if nimberKey not in self.nimberMap:
                    self.nimberMap[nimberKey] = []
                self.nimberMap[nimberKey].append(s)
    
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
            else:
                for i in range(1, heap_sizes[depth] + 1):
                    generate_heaps(current_heaps + [i], depth + 1)
    
        generate_heaps([], 0)
        
    def nimkey(self, state):
        nimberVal = self.nimsum(state)
        return f"nimber_{nimberVal}"
        
    def getEqStates(self, state):
        nimberKey = self.nimkey(state)
        return self.nimberMap.get(nimberKey, [])
        
    def getAbstractQVal(self, state, action):
        baseVal = self.Q.get((tuple(state), action), 0)
        
        if baseVal != 0:
            return baseVal
            
        eqStates = self.getEqStates(state)
        eqVals = []
        
        for eqState in eqStates:
            if eqState == state:
                continue
                
            for a in Nim.avail_acts(eqState):
                if self.isEquivAction(state, action, eqState, a):
                    val = self.Q.get((tuple(eqState), a), 0)
                    if val != 0:
                        eqVals.append(val)
        
        return max(eqVals) if eqVals else 0
    
    def isEquivAction(self, s1, a1, s2, a2):
        p1, c1 = a1
        p2, c2 = a2
        
        s1New = list(s1)
        s1New[p1] -= c1
        
        s2New = list(s2)
        s2New[p2] -= c2
        
        return self.nimsum(s1New) == self.nimsum(s2New)
    
    def pi_s(self, s):
        A = list(Nim.avail_acts(s))
        if random.random() < self.epsilon:
            return random.choice(A)
        return max(A, key=lambda a: self.getAbstractQVal(s, a), default=None)
    
    def MCPolicyEval(self, episode):
        S, A, R = zip(*episode)
        T = len(S) - 1
        G = 0
        visitedPairs = set()
        
        for t in range(T-1, -1, -1):
            s = S[t]
            a = A[t]
            r = R[t]
            G = r + self.alpha * G
            SApair = (tuple(s), a)
            
            self.N[SApair] = self.N.get(SApair, 0) + 1
            self.Q[SApair] = self.Q.get(SApair, 0) + (1.0/self.N[SApair]) * (G - self.Q.get(SApair, 0))
            
            if SApair not in visitedPairs:
                visitedPairs.add(SApair)
                
                nimberKey = self.nimkey(s)
                eqStates = self.nimberMap.get(nimberKey, [])
                
                for eqState in eqStates:
                    if tuple(eqState) == tuple(s):
                        continue
                        
                    for eqAction in Nim.avail_acts(eqState):
                        if self.isEquivAction(s, a, eqState, eqAction):
                            eqSApair = (tuple(eqState), eqAction)
                            self.N[eqSApair] = self.N.get(eqSApair, 0) + 0.5
                            self.Q[eqSApair] = self.Q.get(eqSApair, 0) + (0.5/self.N[eqSApair]) * (G - self.Q.get(eqSApair, 0))
        
        self.k += 1
        self.epsilon = 1.0/self.k
