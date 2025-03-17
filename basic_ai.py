def move():
    global board
    global playerVictory
    tempList = board.copy()
    foundBalanced = False
    
    if random.randint(0, 100) > difficulty:
        if is_balanced(tempList):
            for row in range(4):
                if tempList[row] > 0:
                    tempList[row] -= 1
                    board = tempList.copy()
                    break
        else:
            for row in range(4):
                rowTraversed = row + 1
                if tempList[row] > 0:
                    original_value = tempList[row]
                    for amount in range(1, original_value + 1):
                        tempList[row] = original_value - amount
                        if is_balanced(tempList):
                            MoveMessage = ' removed: ' + str(amount) + ' From row: ' + str(rowTraversed)
                            MovesHistory.append(MoveMessage)
                            board = tempList.copy()
                            foundBalanced = True
                            break
                        
                    if foundBalanced:
                        break
                    tempList[row] = original_value
    else:
        for row in range(4):
            if tempList[row] > 0:
                tempList[row] -= 1
                board = tempList.copy()
                break
