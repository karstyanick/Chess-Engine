from typing import List, Tuple, cast
import tkinter as tk
from functools import partial

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece
import re

from makeMove import makeMove, setCheckMate
import time


class Application(tk.Frame):

    board = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    boardState = board.board
    legalmoves = []

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

    def recordpress(self, position: int):
        pressedButton = self.button_identities[position]
        pressedButtonName = str(pressedButton)
        clickedIndex = int(re.findall(r"\d+", pressedButtonName)[0])

        if self.pickedpiece == "none":
            if (
                self.boardState[clickedIndex] != "none"
                or cast(Piece, self.boardState[clickedIndex]).color != self.nextTurn
            ):
                return

            self.pickedpiece = self.boardState[clickedIndex]

            if self.boardState[clickedIndex] == "none":
                return

            start_time = time.time()
            self.legalmoves = GenerateLegalMoves(
                clickedIndex, self.board, self.boardState, self.movesList
            )
            end_time = time.time()
            print(
                f"Time taken to generate legal moves: {(end_time - start_time) * 1000:.2f} milliseconds"
            )

            for square in self.legalmoves:
                self.button_identities[square].configure(background="red", activebackground="pink")

            photo = tk.PhotoImage(width=1, height=1)
            pressedButton.configure(image=photo)
            pressedButton.image = photo  # type: ignore

            # print(self.board)
        else:
            # Reset the colors of the legal moves
            for square in self.legalmoves:
                legalMoveButton = self.button_identities[square]
                legalMoveButtonColor = (
                    self.original_button_light_square_color
                    if "lightsquare" in legalMoveButton._name  # type: ignore
                    else self.original_button_dark_square_color
                )
                legalMoveButton.configure(
                    background=legalMoveButtonColor,
                    activebackground=self.original_button_active_color,
                )

            if clickedIndex in self.legalmoves:
                boardDifferences = makeMove(
                    self.board,
                    self.boardState,
                    cast(Piece, self.pickedpiece),
                    clickedIndex,
                    self.movesList,
                    True,
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
                    visualSquare.image = photo  # type: ignore

                self.nextTurn = "Black" if self.nextTurn == "White" else "White"
                king = (
                    self.board.whiteKingRef if self.nextTurn == "White" else self.board.blackKingRef
                )

                if setCheckMate(self.board, self.boardState, king):
                    print("Checkmate")
            else:
                pickedPiece = cast(Piece, self.pickedpiece)
                pressedButton = self.button_identities[pickedPiece.position]
                self.boardState[pickedPiece.position] = self.pickedpiece
                photo = tk.PhotoImage(
                    file="./sprites/" + pickedPiece.color + pickedPiece.name + ".png"
                )
                pressedButton.configure(image=photo)
                pressedButton.image = photo  # type: ignore

            self.pickedpiece = "none"

    def createWidgets(self):
        for rank in range(8):
            for phile in range(8):
                piece = self.boardState[rank * 8 + phile]

                # Load the image for the piece, or a transparent placeholder
                photo = (
                    tk.PhotoImage(
                        file="./sprites/"
                        + cast(Piece, piece).color
                        + cast(Piece, piece).name
                        + ".png"
                    )
                    if piece != "none"
                    else tk.PhotoImage(width=1, height=1)
                )

                # Create the button with the appropriate color and image
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

                # Place the button in the grid
                x.grid(column=phile, row=rank)
                x.image = photo  # type: ignore # Keep a reference to the image
                self.button_identities.append(x)


app = Application()
app.mainloop()
