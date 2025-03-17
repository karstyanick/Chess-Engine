from typing import List, Tuple

from Piece import Piece


def feninterpreter(FENstring):
    ranks = FENstring.split("/")

    currentsquare = 1
    board = []

    for rank in ranks:
        for x in rank:

            if x.isnumeric():
                for i in range(currentsquare, currentsquare + int(x)):
                    board.append("none")

                currentsquare += int(x)

            else:
                board.append(x)
                currentsquare += 1

    return board


def translateMoveList(movesList: List[Tuple[Piece, int, int]]):
    translatedMoves = []

    for move in movesList:
        piece, start, end = move
        translatedMoves.append(
            f"{piece.name} from {translateIndexToSquare(start)} to {translateIndexToSquare(end)}"
        )

    return translatedMoves


def translateIndexToSquare(index: int):
    rank = index // 8
    phile = index % 8

    return f"{chr(97 + phile)}{8 - rank}"
