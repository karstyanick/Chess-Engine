from typing import List, Union
from Piece import Piece

BoardState = List[Union[Piece, str]]


class Board:
    whiteKingRef: Piece
    blackKingRef: Piece
    board: BoardState  # A list containing either Piece objects or "none"

    def __init__(self, initBoard: List[str]):
        self.board = []

        for i, square in enumerate(initBoard):
            if square == "none":
                self.board.append("none")
            else:
                if square == "K":
                    whiteKing = Piece(square, i)
                    self.whiteKingRef = whiteKing
                    self.board.append(whiteKing)
                elif square == "k":
                    blackKing = Piece(square, i)
                    self.blackKingRef = blackKing
                    self.board.append(blackKing)
                else:
                    self.board.append(Piece(square, i))
