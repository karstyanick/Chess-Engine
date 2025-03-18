from typing import List
from Piece import Piece


def feninterpreter(FENstring: str) -> List[str]:
    ranks = FENstring.split("/")

    currentsquare = 1
    board: List[str] = []

    for rank in ranks:
        for x in rank:

            if x.isnumeric():
                for _ in range(currentsquare, currentsquare + int(x)):
                    board.append("none")

                currentsquare += int(x)

            else:
                board.append(x)
                currentsquare += 1

    return board


def translateIndexToSquare(index: int):
    rank = index // 8
    phile = index % 8

    return f"{chr(97 + phile)}{8 - rank}"


def generateNotation(
    piece: Piece,
    start: int,
    end: int,
    wasCapture: bool,
    wasKinsideCastle: bool,
    wasQueesideCastle: bool,
    wasEnPassant: bool,
    wasCheck: bool,
) -> str:
    notation = ""

    if wasKinsideCastle:
        return "O-O"
    elif wasQueesideCastle:
        return "O-O-O"
    else:
        if piece.notationName == "p" or piece.notationName == "P":
            if wasCapture:
                    notation += translateIndexToSquare(start)[0] + "x" + translateIndexToSquare(end)
            else:
                notation += translateIndexToSquare(end)
        else:
            if wasCapture:
                notation += piece.notationName.upper() + "x"  + translateIndexToSquare(end)
            else:
                notation += piece.notationName.upper() + translateIndexToSquare(end)

    if wasCheck:
        notation += "+"
    
    return notation
