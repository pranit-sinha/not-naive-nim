import random
import time
import pickle
from nim import Nim
from egreedy import EpsilonGreedyNim

def train(numeps, initialheaps=[1, 3, 5, 7], saveFile="nimAI.pkl"):
    agent = EpsilonGreedyNim()
    
    for i in range(numeps):
        if i % 1000 == 0:
            print(f"Playing training game {i + 1} of {numeps}")
        
        game = Nim(initialheaps)
        ep = []
        
        while True:
            currPlayer = game.player
            s = game.heaps.copy()
            action = agent.pi_s(s)
            
            game.move(action)
            sn = game.heaps.copy()
            
            if game.winner is not None:
                reward = -1 if currPlayer == game.other_plyr(game.winner) else 1
                ep.append((s, action, reward))
                break
            else:
                ep.append((s, action, 0))
                
        # Update agent based on complete ep
        agent.MCPolicyEval(ep)
    
    print(f"Done training after {numeps} eps")
    
    # Save trained model
    with open(saveFile, "wb") as f:
        pickle.dump(agent, f)
    
    return agent

def load(filePath="nimAI.pkl"):
    try:
        with open(filePath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"No saved model found at {filePath}")
        return None

def playNim(agent, humanPlayerIdx=None):
    if humanPlayerIdx is None:
        humanPlayerIdx = random.randint(0, 1)
    
    game = Nim()
    
    while True:
        # Display game s
        print("\nheaps:")
        for i, heap in enumerate(game.heaps):
            print(f"heap {i}: {heap}")
        print()
        
        availActions = Nim.avail_acts(game.heaps)
        time.sleep(0.5)
        
        # Human move
        if game.player == humanPlayerIdx:
            print("Your Turn")
            while True:
                try:
                    heap = int(input("Choose heap: "))
                    count = int(input("Choose Count: "))
                    if (heap, count) in availActions:
                        break
                    print("Invalid move, try again.")
                except ValueError:
                    print("Please enter numbers only.")
        
        # AI move
        else:
            print("AI's Turn")
            heap, count = agent.pi_s(game.heaps, useEpsilon=False)
            print(f"AI chose to take {count} from heap {heap}.")
        
        # Make move
        game.move((heap, count))
        
        # Check for winner
        if game.winner is not None:
            print("\nGAME OVER")
            winner = "Human" if game.winner == humanPlayerIdx else "AI"
            print(f"Winner is {winner}")
            return winner

def evalAgainstRandom(agent, numGames=1000):
    winsVsRandom = 0
    
    for _ in range(numGames):
        game = Nim()
        aiPlayerIdx = random.randint(0, 1)
        
        while game.winner is None:
            if game.player == aiPlayerIdx:
                action = agent.pi_s(game.heaps, useEpsilon=False)
            else:
                # Random player chooses randomly
                actions = list(Nim.avail_acts(game.heaps))
                action = random.choice(actions)
            
            game.move(action)
        
        if game.winner == aiPlayerIdx:
            winsVsRandom += 1
    
    winRate = winsVsRandom / numGames
    print(f"AI win rate against random opponent: {winRate:.4f}")
    return winRate

if __name__ == "__main__":
    # Check if saved model exists
    loadedAgent = load()
    
    if loadedAgent is None:
        print("No saved model found. Training a new one...")
        agent = train(10000)
    else:
        print("Loaded saved model.")
        agent = loadedAgent
    
    # Evaluate against random strategy
    evalAgainstRandom(agent)
    
    # Play against human
    playAgain = "y"
    while playAgain.lower() == "y":
        playNim(agent)
        playAgain = input("Play again? (y/n): ")
