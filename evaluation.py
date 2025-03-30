from math import sqrt
from Board import Board, BoardState
from makeMove import makeMove, revertMove
from GenerateLegalMoves import GenerateAllLegalMoves
from Piece import Piece
from typing import List, Tuple, cast
import random

counter = 0


def counterIncr() -> None:
    global counter
    counter += 1


def FindMove(
    board: Board,
    boardState: BoardState,
    color: str,
    movesList: List[Tuple[Piece, int, int, str]],
    depth: int,
    isBase: bool = False,
    alpha: int = -100000,
    beta: int = 100000,
):
    moves = GenerateAllLegalMoves(board, boardState, color, movesList)

    evaluations: List[Tuple[Piece, int, int]] = []

    if len(moves) == 0:
        # The search might run into checkmate or stalemate
        # We can return none on the piece and dest because we can only run into checkmate if not in base of recursion
        # The base of recursion will always have at least one move as we are checking for checkmate after player moves
        evaluations.append((None, None, -100000)) # type: ignore

    stopLoop = False

    for move in moves:
        piece = move[0]
        for destination in move[1]:

            differences = makeMove(board, boardState, piece, destination, [], False)

            if depth != 0:
                bestOpponentMoveScore = -FindMove(
                    board,
                    boardState,
                    "White" if color == "Black" else "Black",
                    movesList,
                    depth - 1,
                    False,
                    -beta,
                    -alpha,
                )[2]

                counterIncr()

                if bestOpponentMoveScore > alpha:
                    alpha = bestOpponentMoveScore
                    evaluations.append((piece, destination, bestOpponentMoveScore))
                    revertMove(boardState, differences, [])
                    continue

                if bestOpponentMoveScore >= beta:
                    evaluations.append((piece, destination, bestOpponentMoveScore))
                    revertMove(boardState, differences, [])
                    stopLoop = True
                    break

                evaluations.append((piece, destination, -100000)) # This should not update the score but we need to append a value to avoid empty evaluations
            else:
                evaluations.append((piece, destination, EvaluatePosition(board, boardState, color)))
                counterIncr()

            revertMove(boardState, differences, [])
        if stopLoop:
            break

    evaluations.sort(key=lambda x: x[2], reverse=True)
    max_evaluations = [e for e in evaluations if e[2] == evaluations[0][2]]
    chosen_move = random.choice(max_evaluations)
    if isBase:
        print("Chosen move eval: ", chosen_move[2])
        global counter
        print(counter)
        counter = 0
    return chosen_move


def EvaluatePosition(board: Board, boardState: BoardState, color: str) -> int:
    white_value = 0
    black_value = 0

    for piece in boardState:

        if piece == "none":
            continue

        piece = cast(Piece, piece)
       
        if piece.color == "White":
            white_value += piece.value * 100 + AddPieceSquareValuation(board, piece)
        else:
            black_value += piece.value * 100 + AddPieceSquareValuation(board, piece)

    # Return the scaled result
    if color == "White":
        return white_value - black_value
    else:
        return black_value - white_value
    
def AddPieceSquareValuation(board: Board, piece: Piece) -> int:
    if piece.name == "Pawn":
        if piece.color == "White":
            return board.whitePawnSquareTable[piece.position]
        else:
            return board.blackPawnSquareTable[piece.position]
    elif piece.name == "Knight":
        if piece.color == "White":
            return board.whiteKnightSquareTable[piece.position]
        else:
            return board.blackKnighTsquareTable[piece.position]
    elif piece.name == "Bishop":
        if piece.color == "White":
            return board.whiteBishopSquareTable[piece.position]
        else:
            return board.blackBishopSquareTable[piece.position]
    elif piece.name == "Rook":
        if piece.color == "White":
            return board.whiteRookSquareTable[piece.position]
        else:
            return board.blackRookSquareTable[piece.position]
    elif piece.name == "Queen":
        if piece.color == "White":
            return board.whiteQueenSquareTable[piece.position]
        else:
            return board.blackQueenSquareTable[piece.position]
    elif piece.name == "King":
        if piece.color == "White":
            return board.whiteKingSquareTable[piece.position]
        else:
            return board.blackKingSquareTable[piece.position]
    else:
        return 0

def AddCenterValuation(piece: Piece) -> int:
    pos = piece.position
    pieceCoordinates = (pos % 8, pos // 8)
    centralSquares = [(3, 3), (3, 4), (4, 3), (4, 4)]

    distances = [
        sqrt(
            (pieceCoordinates[0] - centralSquare[0]) ** 2
            + (pieceCoordinates[1] - centralSquare[1]) ** 2
        )
        * 10
        for centralSquare in centralSquares
    ]

    max_value = 25
    scaling_factor = 10
    valuation = max_value - int(min(distances) * scaling_factor)

    return max(0, valuation)
