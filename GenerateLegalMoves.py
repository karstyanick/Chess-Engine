
rookmoves = [-8,8,-1,1]
bishopmoves = [-9,-7,9,7]
queenmoves = [-8,8,-1,1,-9,-7,9,7]
whitepawnmoves = [-7,-8,-9]
blackpawnmoves = [7,8,9]
knightmoves = [-6,-10,-15,-17,6,10,15,17]
kingmoves = [-8,8,-1,1,7,-7,9,-9]

def singleSquareMovesToEdge(index):
    NumOfSquaresToEdge = []

    up = int(index/8)
    down = int((63 - index)/8)
    left = int(index % 8)
    right = int(7-(index % 8))
    up_right = int(min(up, right))
    up_left = int(min(up, left))
    down_right = int(min(down, right))
    down_left = int(min(down, left))

    knight_up_right_vert = 1 if up >=2 and right >=1 else 0
    knight_up_right_hori = 1 if up >=1 and right >=2 else 0
    knight_up_left_vert = 1 if up >=2 and left >=1 else 0
    knight_up_left_hori = 1 if up >=1 and left >=2 else 0
    knight_down_right_vert = 1 if down >=2 and right >=1 else 0
    knight_down_right_hori = 1 if down >=1 and right >=2 else 0
    knight_down_left_vert = 1 if down >=2 and left >=1 else 0
    knight_down_left_hori = 1 if down >=1 and left >=2 else 0

    NumOfSquaresToEdge.extend([up, down, left, right, up_right, up_left, down_right, down_left, knight_up_right_vert, knight_up_right_hori, knight_up_left_vert, knight_up_left_hori, knight_down_right_vert, knight_down_right_hori, knight_down_left_vert, knight_down_left_hori])

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


def getDefaultMovesForOffset(Board, Piece, pieceIndex, offset, iters, allowCapture=True):

    legalmovesToAdd = []

    for i in range (0, iters):
        if collision(Board, Piece, pieceIndex, offset)[0]:
            break
        if collision(Board, Piece, pieceIndex, offset)[1]:
            if(allowCapture):
                legalmovesToAdd.append(pieceIndex + offset)
                pieceIndex += offset
            break
                
        legalmovesToAdd.append(pieceIndex + offset)
        pieceIndex += offset
    
    return legalmovesToAdd


def getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset):
    NumOfSquresToEdgeList = singleSquareMovesToEdge(pieceIndex)

    if offset == -8:
        return NumOfSquresToEdgeList[0]
    elif offset == 8:
        return NumOfSquresToEdgeList[1]
    elif offset == -1:
        return NumOfSquresToEdgeList[2]
    elif offset == 1:
        return NumOfSquresToEdgeList[3]
    elif offset == -7:
        return NumOfSquresToEdgeList[4]
    elif offset == -9:
        return NumOfSquresToEdgeList[5]
    elif offset == 9:
        return NumOfSquresToEdgeList[6]
    elif offset == 7:
        return NumOfSquresToEdgeList[7]
    elif offset == -15:
        return NumOfSquresToEdgeList[8]
    elif offset == -6:
        return NumOfSquresToEdgeList[9]
    elif offset == -17:
        return NumOfSquresToEdgeList[10]
    elif offset == -10:
        return NumOfSquresToEdgeList[11]
    elif offset == 17:
        return NumOfSquresToEdgeList[12]
    elif offset == 10:
        return NumOfSquresToEdgeList[13]
    elif offset == 15:
        return NumOfSquresToEdgeList[14]
    elif offset == 6:
        return NumOfSquresToEdgeList[15]


def generateLegalRookMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalBishopMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalQueenMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalBlackPawnMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)


        if (offset == 7 or offset == 9):
            if pieceIndex+offset < 64 and board[pieceIndex+offset] == "none":
                continue
            else:
                legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))
        else:
            legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2 if piece.firstmove else 1), False)

    return legalMoves

def generateLegalWhitePawnMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)

        if (offset == -7 or offset == -9):
            if pieceIndex+offset > 0 and board[pieceIndex+offset] == "none":
                continue
            else:
                legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))
        else:
            legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2 if piece.firstmove else 1), False)

    return legalMoves

def generateLegalKingMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))

    return legalMoves

def generateLegalKnightMoves(piece, board, pieceIndex, moveset):
    legalMoves = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves = legalMoves + getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def GenerateLegalMoves(pieceIndex, board):
    legalmoves = []
    piece = board[pieceIndex]

    if piece.name == "Rook":
        legalmoves = legalmoves + generateLegalRookMoves(piece, board, pieceIndex, rookmoves)
    elif piece.name == "Bishop":
        legalmoves = legalmoves + generateLegalBishopMoves(piece, board, pieceIndex, bishopmoves)
    elif piece.name == "Queen":
        legalmoves = legalmoves + generateLegalQueenMoves(piece, board, pieceIndex, queenmoves)
    elif piece.name == "Pawn" and piece.color == "Black":
        legalmoves = legalmoves + generateLegalBlackPawnMoves(piece, board, pieceIndex, blackpawnmoves)
    elif piece.name == "Pawn" and piece.color == "White":
        legalmoves = legalmoves + generateLegalWhitePawnMoves(piece, board, pieceIndex, whitepawnmoves)
    elif piece.name == "Knight":
        legalmoves = legalmoves + generateLegalKnightMoves(piece, board, pieceIndex, knightmoves)
    elif piece.name == "King":
        legalmoves = legalmoves + generateLegalKingMoves(piece, board, pieceIndex, kingmoves)
  
    piece.firstmove = False
    print(legalmoves)
    print("---------------------------------------------------")
    
    return legalmoves