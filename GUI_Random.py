from typing import List, Tuple
import tkinter as tk
from functools import partial
import random
import re
import time

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves, setCheckMate
from Piece import Piece
from makeMove import makeMove


class Application(tk.Frame):

    boardinit = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    board = boardinit.board
    legalmoves = []

    # Initially, let White move first.
    # Set this variable to the color the human is playing.
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

    def recordpress(self, position):
        if self.nextTurn != self.human_color:
            return
        
        king = next((piece for piece in self.board if piece != "none" and piece.name == "King" and piece.color == self.human_color), None)
        if king.inCheckMate:
            print("Checkmate")
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
                boardDifferences = makeMove(self.board, self.pickedpiece, self.legalmoves, clickedIndex, self.movesList, True)
                for difference in boardDifferences:
                    index, newState = difference
                    if newState == "none":
                        photo = tk.PhotoImage(width=1, height=1)
                    else:
                        photo = tk.PhotoImage(file="./sprites/" + newState.color + newState.name + ".png")

                    visualSquare = self.button_identities[index]
                    visualSquare.configure(image=photo)
                    visualSquare.image = photo

                self.nextTurn = "Black" if self.nextTurn == "White" else "White"
                setCheckMate(self.board, self.nextTurn)
                
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
        computer_color = self.nextTurn

        king = next((piece for piece in self.board if piece != "none" and piece.name == "King" and piece.color == computer_color), None)

        if king.inCheckMate:
            print("Checkmate")
            return

        computerPieces = [piece for piece in self.board if piece != "none" and piece.color == computer_color]

        randomPiece = None
        moves = []

        while len(moves) == 0:
          randomPiece = random.choice(computerPieces)
          moves = GenerateLegalMoves(randomPiece.position, self.board, self.movesList)
        
        destination = random.choice(moves)

        boardDifferences = makeMove(self.board, randomPiece, moves, destination, self.movesList, True)

        for difference in boardDifferences:
            index, newState = difference
            if newState == "none":
                photo = tk.PhotoImage(width=1, height=1)
            else:
                photo = tk.PhotoImage(file="./sprites/" + newState.color + newState.name + ".png")

            visualSquare = self.button_identities[index]
            visualSquare.configure(image=photo)
            visualSquare.image = photo

        self.nextTurn = "Black" if self.nextTurn == "White" else "White"
        setCheckMate(self.board, self.nextTurn)
        

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
