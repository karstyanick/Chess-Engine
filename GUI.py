from typing import List, Tuple
import tkinter as tk
from functools import partial

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece
import re


class Application(tk.Frame):

    boardinit = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    board = boardinit.board
    legalmoves = []

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
        pressedButton = (self.button_identities[position])
        pressedButtonName = str(pressedButton)
        clickedIndex = int(re.findall(r'\d+', pressedButtonName)[0])

        if self.pickedpiece == "none":
            if self.board[clickedIndex] != "none" and self.board[clickedIndex].color != self.nextTurn:
                print("Not your turn")
                return
                
            self.pickedpiece = self.board[clickedIndex]

            if self.board[clickedIndex] == "none":
                print("No piece in that square")
                return

            self.legalmoves = GenerateLegalMoves(clickedIndex, self.board, self.movesList)
            for square in self.legalmoves:
                self.button_identities[square].configure(background = "red", activebackground = "pink")

            self.board[clickedIndex] = "none"

            photo = tk.PhotoImage(width=1, height=1)

            pressedButton.configure(image = photo)
            pressedButton.image = photo

            #print(self.board)
        else:
            for square in self.legalmoves:
                legalMoveButton = self.button_identities[square]
                legalMoveButtonColor = self.original_button_light_square_color if "lightsquare" in legalMoveButton._name else self.original_button_dark_square_color
                legalMoveButton.configure(background = legalMoveButtonColor, activebackground = self.original_button_active_color)
            
            if clickedIndex in self.legalmoves:

                if self.pickedpiece.name == "King" and abs(self.pickedpiece.position - (clickedIndex)) == 2:
                    eligableRooks = [piece for piece in self.board if piece != "none" and piece.name == "Rook" and piece.color == self.pickedpiece.color and piece.firstmove]
                    
                    if self.pickedpiece.position > clickedIndex:
                        eligableRook = next((rook for rook in eligableRooks if clickedIndex > rook.position), None)
                        self.board[clickedIndex+1] = eligableRook
                        movedRookField = (self.button_identities[clickedIndex+1])
                    else:
                        eligableRook = next((rook for rook in eligableRooks if clickedIndex < rook.position), None)
                        self.board[clickedIndex-1] = eligableRook
                        movedRookField = (self.button_identities[clickedIndex-1])
                    
                    self.board[eligableRook.position] = "none"
                    
                    emtpyFieldPhoto = tk.PhotoImage(width=1, height=1)
                    emtpyField = (self.button_identities[eligableRook.position])
                    emtpyField.configure(image = emtpyFieldPhoto)
                    emtpyField.image = emtpyFieldPhoto

                    movedRookFieldPhoto = tk.PhotoImage(file= "./sprites/" + eligableRook.color + eligableRook.name + ".png")
                    movedRookField.configure(image = movedRookFieldPhoto)
                    movedRookField.image = movedRookFieldPhoto

                self.pickedpiece.firstmove = False
                self.nextTurn = "Black" if self.nextTurn == "White" else "White"

                self.movesList.append((self.pickedpiece, self.pickedpiece.position, clickedIndex))
                self.pickedpiece.position = clickedIndex

                print(self.movesList)

                photo = tk.PhotoImage(file= "./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png")
                pressedButton.configure(image = photo)
                pressedButton.image = photo
                self.board[clickedIndex] = self.pickedpiece
            else:
                pressedButton = (self.button_identities[self.pickedpiece.position])
                self.board[self.pickedpiece.position] = self.pickedpiece
                photo = tk.PhotoImage(file= "./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png")
                pressedButton.configure(image = photo)
                pressedButton.image = photo

            self.pickedpiece = "none"

    def createWidgets(self):
        for rank in range(8):
            for phile in range(8):
                piece = self.board[rank * 8 + phile]

                # Load the image for the piece, or a transparent placeholder
                photo = (
                    tk.PhotoImage(file="./sprites/" + piece.color + piece.name + ".png")
                    if piece != "none"
                    else tk.PhotoImage(width=1, height=1)
                )

                # Create the button with the appropriate color and image
                x = tk.Button(
                    self,
                    image=photo,
                    height=70,
                    width=70,
                    bg=self.original_button_light_square_color if (rank + phile) % 2 == 0 else self.original_button_dark_square_color,
                    activebackground=self.original_button_active_color,
                    command=partial(self.recordpress, (rank * 8 + phile)),
                    name=f"lightsquare-{rank*8+phile}" if (rank + phile) % 2 == 0 else f"darksquare-{rank*8+phile}",
                )

                # Place the button in the grid
                x.grid(column=phile, row=rank)
                x.image = photo  # Keep a reference to the image
                self.button_identities.append(x)



app = Application()                       
app.master.title('Sample application')    
app.mainloop()