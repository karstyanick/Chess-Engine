from typing import List, Union
from Piece import Piece

BoardState = List[Union[Piece, str]]

class Board:
    board: BoardState  # A list containing either Piece objects or "none"

    def __init__(self, initBoard: List[str]):
        self.board = []

        for i, square in enumerate(initBoard):
            if square == "none":
                self.board.append("none")
            else:
                self.board.append(Piece(square, i))