import copy
from typing import List, Tuple
import tkinter as tk
from functools import partial
import random
import re
import time

from Board import Board
from FENinterpreter import feninterpreter, translateMoveList
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece
from evaluation import FindMove
from makeMove import makeMove, setCheckMate


class Application(tk.Frame):

    boardinit = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    board = boardinit.board
    legalmoves = []

    # Initially, let White move first.
    # Set  variable to the color the human is playing.
    human_color = "White"
    nextTurn = "White"

    button_identities = []

    pickedpiece = "none"

    original_button_active_color = "lightgray"
    original_button_light_square_color = "white"
    original_button_dark_square_color = "gray"

    movesList: List[Tuple[Piece, int, int]] = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
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
            bg='white',
            fg='black',
            font=("Helvetica", 32),
            justify="center"
        )
        # Use place geometry manager to cover the whole board.
        overlay.place(relx=0.5, rely=0.5, anchor="center")


    def recordpress(self, position):
        if self.gameOver:
            return

        if self.nextTurn != self.human_color:
            return
        
        pressedButton = self.button_identities[position]
        pressedButtonName = str(pressedButton)
        clickedIndex = int(re.findall(r'\d+', pressedButtonName)[0])

        if self.pickedpiece == "none":
            if self.board[clickedIndex] == "none" or self.board[clickedIndex].color != self.human_color:
                return

            self.pickedpiece = self.board[clickedIndex]

            start_time = time.time()
            self.legalmoves = GenerateLegalMoves(clickedIndex, self.board, self.movesList)
            end_time = time.time()
            print(f"Time taken to generate legal moves for player: {(end_time - start_time) * 1000:.2f} milliseconds")

            for square in self.legalmoves:
                self.button_identities[square].configure(background="red", activebackground="pink")

            photo = tk.PhotoImage(width=1, height=1)
            pressedButton.configure(image=photo)
            pressedButton.image = photo

        else:
            for square in self.legalmoves:
                legalMoveButton = self.button_identities[square]
                legalMoveButtonColor = (self.original_button_light_square_color 
                                        if "lightsquare" in legalMoveButton._name 
                                        else self.original_button_dark_square_color)
                legalMoveButton.configure(background=legalMoveButtonColor, activebackground=self.original_button_active_color)

            if clickedIndex in self.legalmoves:
                boardDifferences = makeMove(self.board, self.pickedpiece, clickedIndex, self.movesList, True)
                for difference in boardDifferences:
                    index, newState = difference
                    if newState == "none":
                        photo = tk.PhotoImage(width=1, height=1)
                    else:
                        photo = tk.PhotoImage(file="./sprites/" + newState.color + newState.name + ".png")

                    visualSquare = self.button_identities[index]
                    visualSquare.configure(image=photo)
                    visualSquare.image = photo

                computer_color = "Black" if self.human_color == "White" else "White"
                computer_king = next((piece for piece in self.board if piece != "none" and piece.name == "King" and piece.color == computer_color), None)
                setCheckMate(self.board, computer_king)

                if computer_king.inCheckMate:
                    self.displayGameOver("Game Over: Checkmate! You Win.")
                    print("Checkmate")
                    print(translateMoveList(self.movesList))

                self.nextTurn = "Black" if self.nextTurn == "White" else "White"

                if self.nextTurn != self.human_color:
                    self.after(500, self.computerMove)
            else:
                pressedButton = self.button_identities[self.pickedpiece.position]
                self.board[self.pickedpiece.position] = self.pickedpiece
                photo = tk.PhotoImage(file="./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png")
                pressedButton.configure(image=photo)
                pressedButton.image = photo

            self.pickedpiece = "none"

    def computerMove(self):
        if self.gameOver:
            return
        
        computer_color = "Black" if self.human_color == "White" else "White"
        start_time = time.time()
        chosenPiece, chosenDestination, _ = FindMove(self.board, computer_color, computer_color, self.movesList, 2)
        end_time = time.time()
        print(f"Time taken to generate legal moves for computer: {(end_time - start_time) * 1000:.2f} milliseconds")

        boardDifferences = makeMove(self.board, chosenPiece, chosenDestination, self.movesList, True)

        for difference in boardDifferences:
            index, newState = difference
            if newState == "none":
                photo = tk.PhotoImage(width=1, height=1)
            else:
                photo = tk.PhotoImage(file="./sprites/" + newState.color + newState.name + ".png")

            visualSquare = self.button_identities[index]
            visualSquare.configure(image=photo)
            visualSquare.image = photo

        human_color = "Black" if computer_color == "White" else "White"
        human_king = next((piece for piece in self.board if piece != "none" and piece.name == "King" and piece.color == human_color), None)
        setCheckMate(self.board, human_king)
        
        if human_king.inCheckMate:
            self.displayGameOver("Game Over: Checkmate! You Loose.")
            print("Checkmate")
            print(translateMoveList(self.movesList))
            return

        self.nextTurn = "Black" if self.nextTurn == "White" else "White"


    def createWidgets(self):
        for rank in range(8):
            for phile in range(8):
                piece = self.board[rank * 8 + phile]

                photo = (
                    tk.PhotoImage(file="./sprites/" + piece.color + piece.name + ".png")
                    if piece != "none"
                    else tk.PhotoImage(width=1, height=1)
                )

                x = tk.Button(
                    self,
                    image=photo,
                    height=100,
                    width=100,
                    bg=self.original_button_light_square_color if (rank + phile) % 2 == 0 else self.original_button_dark_square_color,
                    activebackground=self.original_button_active_color,
                    command=partial(self.recordpress, (rank * 8 + phile)),
                    name=f"lightsquare-{rank*8+phile}" if (rank + phile) % 2 == 0 else f"darksquare-{rank*8+phile}",
                )

                x.grid(column=phile, row=rank)
                x.image = photo
                self.button_identities.append(x)


app = Application()
app.master.title('Chess Game')
app.mainloop()
