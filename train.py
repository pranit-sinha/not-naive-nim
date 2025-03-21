import random
import time
import pickle
from nim import Nim
from egreedy import EpsilonGreedyNim

def train(numeps, initialheaps=[1, 3, 5, 7], saveFile="nimAI.pkl"):
    agent = EpsilonGreedyNim()
    
    for _ in range(numeps):
        
        game = Nim(initialheaps)
        ep = []
        
        while True:
            currPlayer = game.player
            s = game.heaps.copy()
            a = agent.pi_s(s)
            
            game.move(a)
            
            if game.winner is not None:
                reward = -1 if currPlayer == game.other_plyr(game.winner) else 1
                ep.append((s, a, reward))
                break
            else:
                ep.append((s, a, 0))
                
        agent.MCPolicyEval(ep)
    
    with open(saveFile, "wb") as f:
        pickle.dump(agent, f)
    
    return agent

def playNim(agent, humanPlayerIdx=None):
    if humanPlayerIdx is None:
        humanPlayerIdx = random.randint(0, 1)
    
    game = Nim()
    
    while True:
        print("\nheaps:")
        for i, heap in enumerate(game.heaps):
            print(f"heap {i}: {heap}")
        print()
        
        availA = Nim.avail_acts(game.heaps)
        time.sleep(0.5)
        if game.player == humanPlayerIdx:
            print("Your Turn")
            while True:
                try:
                    heap = int(input("Choose heap: "))
                    count = int(input("Choose Count: "))
                    if (heap, count) in availA:
                        break
                    print("Invalid move, try again.")
                except ValueError:
                    print("Please enter numbers only.")
        
        else:
            print("AI's Turn")
            heap, count = agent.pi_s(game.heaps)
            print(f"AI chose to take {count} from heap {heap}.")
        
        game.move((heap, count))
        
        if game.winner is not None:
            print("\nGAME OVER")
            winner = "Human" if game.winner == humanPlayerIdx else "AI"
            print(f"Winner is {winner}")
            return winner

