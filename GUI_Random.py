from typing import List, Tuple, cast
import tkinter as tk
from functools import partial
import random
import re
import time

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece
from makeMove import makeMove, setCheckMate


class Application(tk.Frame):

    board = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    boardState = board.board
    legalmoves = []

    # Initially, let White move first.
    # Set  variable to the color the human is playing.
    human_color = "White"
    nextTurn = "White"

    button_identities: List[tk.Button] = []

    pickedpiece = "none"

    original_button_active_color = "lightgray"
    original_button_light_square_color = "white"
    original_button_dark_square_color = "gray"

    movesList: List[Tuple[Piece, int, int, str]] = []

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid(column=0, row=0)
        self.createWidgets()
        self.gameOver = False  # Flag to keep track of game state

    def displayGameOver(self, message: str):
        """Display a translucent overlay with a game over message and disable the board."""
        # Set game over flag to True so further clicks are ignored.
        self.gameOver = True

        # Create an overlay Label that covers the entire frame.
        overlay = tk.Label(
            self,
            text=message,
            bg="white",
            fg="black",
            font=("Helvetica", 32),
            justify="center",
        )
        # Use place geometry manager to cover the whole board.
        overlay.place(relx=0.5, rely=0.5, anchor="center")

    def recordpress(self, position: int):
        if self.gameOver:
            return

        if self.nextTurn != self.human_color:
            return

        pressedButton = self.button_identities[position]
        pressedButtonName = str(pressedButton)
        clickedIndex = int(re.findall(r"\d+", pressedButtonName)[0])

        if self.pickedpiece == "none":
            self.pickedpiece = cast(str, self.pickedpiece)

            if (
                self.boardState[clickedIndex] == "none"
                or cast(Piece, self.boardState[clickedIndex]).color != self.human_color
            ):
                return

            self.pickedpiece = self.boardState[clickedIndex]

            start_time = time.time()
            self.legalmoves = GenerateLegalMoves(
                clickedIndex, self.board, self.boardState, self.movesList
            )
            end_time = time.time()
            print(
                f"Time taken to generate legal moves for player: {(end_time - start_time) * 1000:.2f} milliseconds"
            )

            for square in self.legalmoves:
                self.button_identities[square].configure(
                    background="red", activebackground="pink"
                )

            photo = tk.PhotoImage(width=1, height=1)
            pressedButton.configure(image=photo)
            pressedButton.image = photo # type: ignore

        else:
            self.pickedpiece = cast(Piece, self.pickedpiece)

            for square in self.legalmoves:
                legalMoveButton = self.button_identities[square]
                legalMoveButtonColor = (
                    self.original_button_light_square_color
                    if "lightsquare" in legalMoveButton._name # type: ignore
                    else self.original_button_dark_square_color
                )
                legalMoveButton.configure(
                    background=legalMoveButtonColor,
                    activebackground=self.original_button_active_color,
                )

            if clickedIndex in self.legalmoves:
                boardDifferences = makeMove(
                    self.board, self.boardState, self.pickedpiece, clickedIndex, self.movesList, True
                )
                for difference in boardDifferences:
                    index, newState, _ = difference
                    if newState == "none":
                        photo = tk.PhotoImage(width=1, height=1)
                    else:
                        newState = cast(Piece, newState)
                        photo = tk.PhotoImage(
                            file="./sprites/" + newState.color + newState.name + ".png"
                        )

                    visualSquare = self.button_identities[index]
                    visualSquare.configure(image=photo)
                    visualSquare.image = photo # type: ignore

                computer_color = "Black" if self.human_color == "White" else "White"
                
                computer_king = cast(Piece, next(
                    (
                        cast(Piece, piece)
                        for piece in self.boardState
                        if piece != "none"
                        and cast(Piece, piece).name == "King"
                        and cast(Piece, piece).color == computer_color
                    ),
                    None,
                ))
                
                setCheckMate(self.board, self.boardState, computer_king)

                if computer_king.inCheckMate:
                    self.displayGameOver("Game Over: Checkmate! You Win.")
                    print("Checkmate")

                self.nextTurn = "Black" if self.nextTurn == "White" else "White"

                if self.nextTurn != self.human_color:
                    self.after(500, self.computerMove)
            else:
                pressedButton = self.button_identities[self.pickedpiece.position]
                self.boardState[self.pickedpiece.position] = self.pickedpiece
                photo = tk.PhotoImage(
                    file="./sprites/"
                    + self.pickedpiece.color
                    + self.pickedpiece.name
                    + ".png"
                )
                pressedButton.configure(image=photo)
                pressedButton.image = photo # type: ignore

            self.pickedpiece = "none"

    def computerMove(self):
        if self.gameOver:
            return

        computer_color = self.nextTurn

        computerPieces = [
            cast(Piece, piece)
            for piece in self.boardState
            if piece != "none" and cast(Piece, piece).color == computer_color
        ]

        randomPiece = None
        moves: List[int] = []

        while len(moves) == 0:
            randomPiece = random.choice(computerPieces)
            moves = GenerateLegalMoves(randomPiece.position, self.board, self.boardState, self.movesList)

        destination = random.choice(moves)

        boardDifferences = makeMove(
            self.board, self.boardState, cast(Piece, randomPiece), destination, self.movesList, True
        )

        for difference in boardDifferences:
            index, newState, _ = difference
            if newState == "none":
                photo = tk.PhotoImage(width=1, height=1)
            else:
                newState = cast(Piece, newState)
                photo = tk.PhotoImage(
                    file="./sprites/" + newState.color + newState.name + ".png"
                )

            visualSquare = self.button_identities[index]
            visualSquare.configure(image=photo)
            visualSquare.image = photo # type: ignore

        human_color = "Black" if computer_color == "White" else "White"
        human_king = cast(Piece, next(
            (
                cast(Piece, piece)
                for piece in self.boardState
                if piece != "none"
                and cast(Piece, piece).name == "King"
                and cast(Piece, piece).color == human_color
            ),
            None,
        ))

        setCheckMate(self.board, self.boardState, human_king)

        if human_king.inCheckMate:
            self.displayGameOver("Game Over: Checkmate! You Loose.")
            print("Checkmate")
            return

        self.nextTurn = "Black" if self.nextTurn == "White" else "White"

    def createWidgets(self):
        for rank in range(8):
            for phile in range(8):
                piece = self.boardState[rank * 8 + phile]

                if piece == "none":
                    photo = tk.PhotoImage(width=1, height=1)
                else:
                    piece = cast(Piece, piece)
                    photo = tk.PhotoImage(
                        file="./sprites/" + piece.color + piece.name + ".png"
                    )

                x = tk.Button(
                    self,
                    image=photo,
                    height=100,
                    width=100,
                    bg=(
                        self.original_button_light_square_color
                        if (rank + phile) % 2 == 0
                        else self.original_button_dark_square_color
                    ),
                    activebackground=self.original_button_active_color,
                    command=partial(self.recordpress, (rank * 8 + phile)),
                    name=(
                        f"lightsquare-{rank*8+phile}"
                        if (rank + phile) % 2 == 0
                        else f"darksquare-{rank*8+phile}"
                    ),
                )

                x.grid(column=phile, row=rank)
                x.image = photo # type: ignore
                self.button_identities.append(x)


app = Application()
app.mainloop()
