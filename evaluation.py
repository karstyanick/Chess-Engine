from math import sqrt
from makeMove import makeMove
from GenerateLegalMoves import GenerateAllLegalMoves
from Piece import Piece
from typing import List, Tuple, Union, cast
import copy
import random


def FindMove(
    board: List[Union[Piece, str]],
    movesColor: str,
    evaluationColor: str,
    movesList: List[Tuple[Piece, int, int]],
    depth: int,
):
    moves = GenerateAllLegalMoves(board, movesColor, movesList)
    evaluations: List[Tuple[Piece, int, int]] = []

    for move in moves:
        piece = move[0]
        for destination in move[1]:
            boardCopy = copy.deepcopy(board)
            pieceCopy = cast(Piece, boardCopy[piece.position])

            makeMove(boardCopy, pieceCopy, destination, [], False)
            if depth != 0:
                bestOpponentResponse = FindMove(
                    boardCopy,
                    "White" if movesColor == "Black" else "Black",
                    "White" if movesColor == "Black" else "Black",
                    movesList,
                    depth - 1,
                )
                makeMove(
                    boardCopy,
                    bestOpponentResponse[0],
                    bestOpponentResponse[1],
                    [],
                    False,
                )
                evaluations.append(
                    (piece, destination, EvaluatePosition(boardCopy, evaluationColor))
                )
            else:
                evaluations.append(
                    (piece, destination, EvaluatePosition(boardCopy, evaluationColor))
                )

    evaluations.sort(key=lambda x: x[2], reverse=True)
    max_evaluations = [e for e in evaluations if e[2] == evaluations[0][2]]
    return random.choice(max_evaluations)


def EvaluatePosition(board: List[Union[Piece, str]], color: str) -> int:
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
