from Piece import Piece

class Board:
    board = []

    def __init__(self, board):
        self.board = board

        for i, square in enumerate(self.board):
            if square != "none":
                board[i] = Piece(square,i)
            else:
                continue

            