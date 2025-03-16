from typing import List, Union, Tuple
from Piece import Piece
from makeMove import makeMove, revertMove
import copy


# Movesets as lists of integers
rookmoves: List[int] = [-8, 8, -1, 1]
bishopmoves: List[int] = [-9, -7, 9, 7]
queenmoves: List[int] = [-8, 8, -1, 1, -9, -7, 9, 7]
whitepawnmoves: List[int] = [-7, -8, -9]
blackpawnmoves: List[int] = [7, 8, 9]
knightmoves: List[int] = [-6, -10, -15, -17, 6, 10, 15, 17]
kingmoves: List[int] = [-8, 8, -1, 1, 7, -7, 9, -9]

def singleSquareMovesToEdge(index: int) -> List[int]:
    NumOfSquaresToEdge: List[int] = []

    up = int(index / 8)
    down = int((63 - index) / 8)
    left = int(index % 8)
    right = int(7 - (index % 8))
    up_right = int(min(up, right))
    up_left = int(min(up, left))
    down_right = int(min(down, right))
    down_left = int(min(down, left))

    knight_up_right_vert = 1 if up >= 2 and right >= 1 else 0
    knight_up_right_hori = 1 if up >= 1 and right >= 2 else 0
    knight_up_left_vert = 1 if up >= 2 and left >= 1 else 0
    knight_up_left_hori = 1 if up >= 1 and left >= 2 else 0
    knight_down_right_vert = 1 if down >= 2 and right >= 1 else 0
    knight_down_right_hori = 1 if down >= 1 and right >= 2 else 0
    knight_down_left_vert = 1 if down >= 2 and left >= 1 else 0
    knight_down_left_hori = 1 if down >= 1 and left >= 2 else 0

    NumOfSquaresToEdge.extend([
        up, down, left, right, up_right, up_left, down_right, down_left,
        knight_up_right_vert, knight_up_right_hori, knight_up_left_vert, knight_up_left_hori,
        knight_down_right_vert, knight_down_right_hori, knight_down_left_vert, knight_down_left_hori
    ])

    return NumOfSquaresToEdge

def collision(Board: List[Union[Piece, str]], Piece: Piece, index: int, offset: int) -> List[bool]:
    collisionlist: List[bool] = [False, False]

    if 0 <= index + offset < 64 and Board[index + offset] != "none":
        if Piece.color != Board[index + offset].color:
            collisionlist[1] = True
        else:
            collisionlist[0] = True
        return collisionlist
    else:
        return collisionlist

def getDefaultMovesForOffset(Board: List[Union[Piece, str]], Piece: Piece, pieceIndex: int, offset: int, iters: int, allowCapture: bool = True) -> List[int]:
    legalmovesToAdd: List[int] = []

    for _ in range(iters):
        if collision(Board, Piece, pieceIndex, offset)[0]:
            break
        if collision(Board, Piece, pieceIndex, offset)[1]:
            if allowCapture:
                legalmovesToAdd.append(pieceIndex + offset)
                pieceIndex += offset
            break

        legalmovesToAdd.append(pieceIndex + offset)
        pieceIndex += offset

    return legalmovesToAdd

def getNumSquaresToEdgeBasedOnOffset(pieceIndex: int, offset: int) -> int:
    NumOfSquresToEdgeList: List[int] = singleSquareMovesToEdge(pieceIndex)

    offset_map = {
        -8: 0, 8: 1, -1: 2, 1: 3,
        -7: 4, -9: 5, 9: 6, 7: 7,
        -15: 8, -6: 9, -17: 10, -10: 11,
        17: 12, 10: 13, 15: 14, 6: 15
    }

    return NumOfSquresToEdgeList[offset_map[offset]]

def generateLegalRookMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalBishopMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalQueenMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def generateLegalBlackPawnMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int], previousMovesList: List[Tuple[Piece, int, int]]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)

        if offset in [7, 9]:
            if len(previousMovesList) > 0 and previousMovesList[-1][0].name == "Pawn" and (previousMovesList[-1][2]-previousMovesList[-1][1])/8 == 2 and previousMovesList[-1][2]+8 == pieceIndex + offset:
                legalMoves.append(pieceIndex + offset)

            if pieceIndex + offset < 64 and board[pieceIndex + offset] == "none":
                continue
            else:
                legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))
        else:
            legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2 if piece.firstmove else 1), False)

    return legalMoves

def generateLegalWhitePawnMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int], previousMovesList: List[Tuple[Piece, int, int]]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)

        if offset in [-7, -9]:
            if len(previousMovesList) > 0 and previousMovesList[-1][0].name == "Pawn" and (previousMovesList[-1][2]-previousMovesList[-1][1])/8 == 2 and previousMovesList[-1][2]-8 == pieceIndex + offset:
                legalMoves.append(pieceIndex + offset)

            if pieceIndex + offset > 0 and board[pieceIndex + offset] == "none":
                continue
            else:
                legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))
        else:
            legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2 if piece.firstmove else 1), False)

    return legalMoves

def generateLegalKingMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int]) -> List[int]:
    legalMoves: List[int] = []
    eligableRooks = [boardPiece for boardPiece in board if boardPiece != "none" and boardPiece.name == "Rook" and boardPiece.color == piece.color and boardPiece.firstmove and piece.firstmove]

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        if offset == -1 and next((rook for rook in eligableRooks if piece.position > rook.position), None) and piece.firstmove:
                legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2))
        elif offset == 1 and next((rook for rook in eligableRooks if piece.position < rook.position), None) and piece.firstmove:
                legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 2))
        else:
            legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, min(numberOfSquaresToEdge, 1))

    return legalMoves

def generateLegalKnightMoves(piece: Piece, board: List[Union[Piece, str]], pieceIndex: int, moveset: List[int]) -> List[int]:
    legalMoves: List[int] = []

    for offset in moveset:
        numberOfSquaresToEdge = getNumSquaresToEdgeBasedOnOffset(pieceIndex, offset)
        legalMoves += getDefaultMovesForOffset(board, piece, pieceIndex, offset, numberOfSquaresToEdge)

    return legalMoves

def GenerateLegalMovesPreCheck(pieceIndex: int, board: List[Union[Piece, str]], previousMovesList: List[Tuple[Piece, int, int]]) -> List[int]:
    legalmoves: List[int] = []
    piece = board[pieceIndex]

    if piece.name == "Rook":
        legalmoves += generateLegalRookMoves(piece, board, pieceIndex, rookmoves)
    elif piece.name == "Bishop":
        legalmoves += generateLegalBishopMoves(piece, board, pieceIndex, bishopmoves)
    elif piece.name == "Queen":
        legalmoves += generateLegalQueenMoves(piece, board, pieceIndex, queenmoves)
    elif piece.name == "Pawn" and piece.color == "Black":
        legalmoves += generateLegalBlackPawnMoves(piece, board, pieceIndex, blackpawnmoves, previousMovesList)
    elif piece.name == "Pawn" and piece.color == "White":
        legalmoves += generateLegalWhitePawnMoves(piece, board, pieceIndex, whitepawnmoves, previousMovesList)
    elif piece.name == "Knight":
        legalmoves += generateLegalKnightMoves(piece, board, pieceIndex, knightmoves)
    elif piece.name == "King":
        legalmoves += generateLegalKingMoves(piece, board, pieceIndex, kingmoves)
    
    return legalmoves

def GenerateLegalMoves(pieceIndex: int, board: List[Union[Piece, str]], previousMovesList: List[Tuple[Piece, int, int]]) -> List[int]:
    legalmoves = GenerateLegalMovesPreCheck(pieceIndex, board, previousMovesList)
    piece = board[pieceIndex]

    for move in legalmoves[:]:
        differences = makeMove(board, piece, move, previousMovesList, False)
        if next((boardPiece for boardPiece in board if boardPiece != "none" and boardPiece.name == "King" and boardPiece.color == piece.color and boardPiece.inCheck), None):
            legalmoves.remove(move)
        revertMove(board, differences, previousMovesList)
        
    if (piece.name == "King" and piece.position + 2 in legalmoves and piece.position + 1 not in legalmoves):
        legalmoves.remove(piece.position + 2)

    if (piece.name == "King" and piece.position - 2 in legalmoves and piece.position - 1 not in legalmoves):
        legalmoves.remove(piece.position - 2)

    return legalmoves

def GenerateAllLegalMoves(board: List[Union[Piece, str]], color: str, previousMovesList: List[Tuple[Piece, int, int]]) -> List[Tuple[Piece, List[int]]]:
    legalmoves: List[Tuple[Piece, List[int]]] = []

    for index, piece in enumerate(board):
        if piece != "none" and piece.color == color:
            foundMoves = GenerateLegalMoves(index, board, previousMovesList)
            if len(foundMoves) > 0:
                legalmoves.append((piece, foundMoves))
    
    return legalmoves