
rookmoves = [-8,8,-1,1]
bishopmoves = [-9,-7,9,7]
queenmoves = [-8,8,-1,1,-9,-7,9,7]
whitepawnmoves = [-7,-8,-9]
blackpawnmoves = [7,8,9]
knightmoves = [-6,-10,-15,-17,6,10,15,17]
kingmoves = [-8,8,-1,1,7,-7,9,-9]

def SquaresToEdge(index):
    NumOfSquaresToEdge = []

    up = int(index/8)
    down = int((63 - index)/8)
    left = int(index % 8)
    right = int(7-(index % 8))
    up_right = int(min(up, right))
    up_left = int(min(up, left))
    down_right = int(min(down, right))
    down_left = int(min(down, left))

    NumOfSquaresToEdge.extend([up, down, left, right, up_right, up_left, down_right, down_left])
    return NumOfSquaresToEdge

def collision(Board, Piece, index, offset):
    collisionlist = [False, False]

    if index+offset < 64 and index+offset > 0 and Board[index+offset] != "none":
        if Piece.color != Board[index+offset].color:
            collisionlist[1] = True
        else:
            collisionlist[0] = True
        return collisionlist
    else:
        return collisionlist


def GenerateLegalMoves(PieceIndex, Board):
    legalmoves = []
    Piece = Board[PieceIndex]
    kingmove = False

    if Piece.name == "Rook":
        moveset = rookmoves
    elif Piece.name == "Bishop":
        moveset = bishopmoves
    elif Piece.name == "Queen":
        moveset = queenmoves
    elif Piece.name == "Pawn" and Piece.color == "Black":
        moveset = blackpawnmoves
    elif Piece.name == "Pawn" and Piece.color == "White":
        moveset = whitepawnmoves
    elif Piece.name == "Knight":
        moveset = knightmoves
    elif Piece.name == "King":
        moveset = kingmoves

    

    for offset in moveset:

        index = PieceIndex
        NumOfSquresToEdgeList =  SquaresToEdge(index)

        if offset < 0:
            if offset == -8:
                NumOfSquresToEdge = NumOfSquresToEdgeList[0]
                if moveset == whitepawnmoves:
                    pawnmoves = 1
                    if Piece.firstmove:
                        pawnmoves = 2
                        Piece.firstmove = False
                    for i in range (0, min(NumOfSquresToEdge, pawnmoves)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            break

                        legalmoves.append(index + offset)
                        index += offset

                elif moveset == kingmoves:

                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset
                
            elif offset == -1:
                NumOfSquresToEdge = NumOfSquresToEdgeList[2]
                if moveset == kingmoves:
                    x = 1
                    if Piece.firstmove and Board[63].firstmove:
                        x = 2
                    for i in range (0, min(NumOfSquresToEdge, x)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                        index += offset
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                        legalmoves.append(index + offset)
                        index += offset

            elif offset == -7:
                NumOfSquresToEdge = NumOfSquresToEdgeList[4]
                if moveset == whitepawnmoves:
                    if index+offset < 64 and index+offset > 0 and Board[index+offset] != "none":
                        for i in range (0, min(NumOfSquresToEdge, 1)):
                            if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                            legalmoves.append(index + offset)
                            index += offset
                    else:
                        continue
                elif moveset == kingmoves:

                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset

            elif offset == -9:
                NumOfSquresToEdge = NumOfSquresToEdgeList[5]
                if moveset == whitepawnmoves:
                    if index+offset < 64 and index+offset > 0 and  Board[index+offset] != "none":
                        for i in range (0, min(NumOfSquresToEdge, 1)):
                            if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                            legalmoves.append(index + offset)
                            index += offset
                    else:
                        continue

                elif moveset == kingmoves:
 
                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset

            elif offset == -6:
                NumOfSquresToEdgeUp = NumOfSquresToEdgeList[0]
                NumOfSquresToEdgeRight = NumOfSquresToEdgeList[3]

                if(NumOfSquresToEdgeUp >= 1 and NumOfSquresToEdgeRight >= 2):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == -10:
                NumOfSquresToEdgeUp = NumOfSquresToEdgeList[0]
                NumOfSquresToEdgeLeft = NumOfSquresToEdgeList[2]

                if(NumOfSquresToEdgeUp >= 1 and NumOfSquresToEdgeLeft >= 2):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == -15:
                NumOfSquresToEdgeUp = NumOfSquresToEdgeList[0]
                NumOfSquresToEdgeRight = NumOfSquresToEdgeList[3]

                if(NumOfSquresToEdgeUp >= 2 and NumOfSquresToEdgeRight >= 1):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == -17:
                NumOfSquresToEdgeUp = NumOfSquresToEdgeList[0]
                NumOfSquresToEdgeLeft = NumOfSquresToEdgeList[2]

                if(NumOfSquresToEdgeUp >= 2 and NumOfSquresToEdgeLeft >= 1):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)
        else:
            if offset == 8:
                NumOfSquresToEdge = NumOfSquresToEdgeList[1]

                if moveset == blackpawnmoves:
                    pawnmoves = 1
                    if Piece.firstmove:
                        pawnmoves = 2
                        Piece.firstmove = False

                    for i in range (0, min(NumOfSquresToEdge, pawnmoves)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            break

                        legalmoves.append(index + offset)
                        index += offset

                elif moveset == kingmoves:

                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset
            elif offset == 1:

                NumOfSquresToEdge = NumOfSquresToEdgeList[3]
                
                if moveset == kingmoves:
                    x = 1
                    if Piece.firstmove and Board[63].firstmove:
                        x = 2
                        Piece.firstmove = False
                        Board[63].firstmove = False
                    for i in range (0, min(NumOfSquresToEdge, x)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                        index+=offset
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                        legalmoves.append(index + offset)
                        index += offset

            elif offset == 7:
                NumOfSquresToEdge = NumOfSquresToEdgeList[7]

                if moveset == blackpawnmoves:
                    if index+offset < 64 and index+offset > 0 and Board[index+offset] != "none":
                        for i in range (0, min(NumOfSquresToEdge, 1)):
                            if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                            legalmoves.append(index + offset)
                            index += offset
                    else:
                        continue
                elif moveset == kingmoves:

                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset
            elif offset == 9:
                NumOfSquresToEdge = NumOfSquresToEdgeList[6]

                if moveset == blackpawnmoves:
                    if index+offset < 64 and index+offset > 0 and Board[index+offset] != "none":
                        for i in range (0, min(NumOfSquresToEdge, 1)):
                            if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                                if collision(Board, Piece, index, offset)[0]:
                                    break
                                else:
                                    legalmoves.append(index + offset)
                                    index += offset
                                    break
                            legalmoves.append(index + offset)
                            index += offset
                    else:
                        continue
                elif moveset == kingmoves:

                    for i in range (0, min(NumOfSquresToEdge, 1)):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                        legalmoves.append(index+offset)
                else:
                    for i in range (0,NumOfSquresToEdge):
                        if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                break
                            else:
                                legalmoves.append(index + offset)
                                index += offset
                                break
                        legalmoves.append(index + offset)
                        index += offset

            elif offset == 6:
                NumOfSquresToEdgeDown = NumOfSquresToEdgeList[1]
                NumOfSquresToEdgeLeft = NumOfSquresToEdgeList[2]

                if(NumOfSquresToEdgeDown >= 1 and NumOfSquresToEdgeLeft >= 2):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == 10:
                NumOfSquresToEdgeDown = NumOfSquresToEdgeList[1]
                NumOfSquresToEdgeRight = NumOfSquresToEdgeList[3]

                if(NumOfSquresToEdgeDown >= 1 and NumOfSquresToEdgeRight >= 2):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == 15:
                NumOfSquresToEdgeDown = NumOfSquresToEdgeList[1]
                NumOfSquresToEdgeLeft = NumOfSquresToEdgeList[2]

                if(NumOfSquresToEdgeDown >= 2 and NumOfSquresToEdgeLeft >= 1):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)

            elif offset == 17:
                NumOfSquresToEdgeDown = NumOfSquresToEdgeList[1]
                NumOfSquresToEdgeRight = NumOfSquresToEdgeList[3]

                if(NumOfSquresToEdgeDown >= 2 and NumOfSquresToEdgeRight >= 1):
                    if collision(Board, Piece, index, offset)[0] or collision(Board, Piece, index, offset)[1]:
                            if collision(Board, Piece, index, offset)[0]:
                                continue
                            else:
                                legalmoves.append(index + offset)
                                continue
                    legalmoves.append(index+offset)
    
    print(legalmoves)
    print("---------------------------------------------------")
    
    return legalmoves