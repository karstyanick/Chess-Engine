from Board import Board, BoardState
from makeMove import makeMove, revertMove
from GenerateLegalMoves import GenerateAllLegalMoves
from Piece import Piece
from typing import List, Tuple
import random

counter = 0


def FindMove(
    board: Board,
    boardState: BoardState,
    movesColor: str,
    evaluationColor: str,
    movesList: List[Tuple[Piece, int, int, str]],
    depth: int,
    isBase: bool = False,
    previousBestEval: int = -1000000,
):
    global counter
    moves = GenerateAllLegalMoves(board, boardState, movesColor, movesList)
    evaluations: List[Tuple[Piece, int, int]] = []

    for move in moves:
        piece = move[0]
        for destination in move[1]:

            outer_differences = makeMove(board, boardState, piece, destination, [], False)

            if depth != 0:
                bestOpponentResponse = FindMove(
                    board,
                    boardState,
                    "White" if movesColor == "Black" else "Black",
                    "White" if movesColor == "Black" else "Black",
                    movesList,
                    depth - 1,
                    False,
                    previousBestEval,
                )
                inner_differences = makeMove(
                    board,
                    boardState,
                    bestOpponentResponse[0],
                    bestOpponentResponse[1],
                    [],
                    False,
                )

                newBestEval = EvaluatePosition(boardState, evaluationColor)

                if previousBestEval < newBestEval:
                    previousBestEval = newBestEval
                    evaluations.append((piece, destination, newBestEval))

                counterIncr()
                revertMove(boardState, inner_differences, [])
            else:
                opponentResponse = EvaluatePosition(boardState, evaluationColor)

                if previousBestEval != -1000000 and opponentResponse < previousBestEval:
                    revertMove(boardState, outer_differences, [])
                    return (piece, destination, -1000000)
                else:
                    evaluations.append((piece, destination, opponentResponse))
                    counterIncr()

            revertMove(boardState, outer_differences, [])

    evaluations.sort(key=lambda x: x[2], reverse=True)
    max_evaluations = [e for e in evaluations if e[2] == evaluations[0][2]]
    if isBase:
        print(counter)
        counter = 0
    return random.choice(max_evaluations)
