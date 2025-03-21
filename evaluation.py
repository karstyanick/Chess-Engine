from math import sqrt
from Board import BoardState
from makeMove import makeMove, revertMove
from GenerateLegalMoves import GenerateAllLegalMoves
from Piece import Piece
from typing import List, Tuple, cast
import random

counter = 0

def counterIncr () -> None:
    global counter
    counter += 1 # type: ignore

def FindMove(
    board: BoardState,
    movesColor: str,
    evaluationColor: str,
    movesList: List[Tuple[Piece, int, int, str]],
    depth: int,
    isBase: bool = False,
    previousMaxEval: int = -100000
):
    moves = GenerateAllLegalMoves(board, movesColor, movesList)
    evaluations: List[Tuple[Piece, int, int]] = []

    for move in moves:
        piece = move[0]
        for destination in move[1]:

            differences = makeMove(board, piece, destination, [], False)
            
            if depth != 0:
                bestOpponentResponse = FindMove(
                    board,
                    "White" if movesColor == "Black" else "Black",
                    "White" if movesColor == "Black" else "Black",
                    movesList,
                    depth - 1,
                )
                innerDiff = makeMove(
                    board,
                    bestOpponentResponse[0],
                    bestOpponentResponse[1],
                    [],
                    False,
                )
                counterIncr()
                if(bestOpponentResponse[2] > previousMaxEval):
                    previousMaxEval = bestOpponentResponse[2]

                evaluation = EvaluatePosition(board, evaluationColor)
                
                if evaluation < previousMaxEval:
                    revertMove(board, innerDiff, [])
                    revertMove(board, differences, [])
                    break
                else:
                    evaluations.append((piece, destination, evaluation))
                    revertMove(board, innerDiff, [])
            else:
                evaluations.append(
                    (piece, destination, EvaluatePosition(board, evaluationColor))
                )
                counterIncr()
            
            revertMove(board, differences, [])

    evaluations.sort(key=lambda x: x[2], reverse=True)
    max_evaluations = [e for e in evaluations if e[2] == evaluations[0][2]]
    if(isBase):
        global counter
        print(counter)
        counter = 0
    return random.choice(max_evaluations)


def EvaluatePosition(board: BoardState, color: str) -> int:
    white_value = 0
    black_value = 0

    for piece in board:

        if piece == "none":
            continue

        piece = cast(Piece, piece)

        # Skip empty squares and kings if required
        if piece.name != "King":
            # Multiply the piece value by 100 to match the scaling
            if piece.color == "White":
                white_value += piece.value * 100 + AddCenterValuation(piece)
            else:
                black_value += piece.value * 100 + AddCenterValuation(piece)

    # Return the scaled result
    if color == "White":
        return white_value - black_value
    else:
        return black_value - white_value


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
