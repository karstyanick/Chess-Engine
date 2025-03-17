from typing import List, Union
from Piece import Piece


class Board:
    board: List[Union[Piece, str]]  # A list containing either Piece objects or "none"

    def __init__(self, board: List[Union[Piece, str]]):
        self.board = board

        for i, square in enumerate(self.board):
            if square != "none":
                self.board[i] = Piece(square, i)  # Replace with a Piece object
            else:
                continue
