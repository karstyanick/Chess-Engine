import tkinter as tk
from functools import partial

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece


class Application(tk.Frame):

    boardinit = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    board = boardinit.board
    legalmoves = []


    button_identities = []

    pickedpiece = "none"
    pickedindex = 0

    def __init__(self, master=None):

        tk.Frame.__init__(self, master) 
        self.grid(column=0, row=0)                       
        self.createWidgets()

    def recordpress(self, position):
        bname = (self.button_identities[position])
        bnamestr = str(bname)

        if len(bnamestr) > 21 and len(bnamestr) <= 22:
            index = int(bnamestr[21])
        elif len(bnamestr) > 22:
            index = int(bnamestr[21] + "" + str(bnamestr)[22])
        else:
            index = 1

        if self.pickedpiece == "none":
            self.pickedpiece = self.board[index-1]
            self.pickedindex = index-1
            self.legalmoves = GenerateLegalMoves(index-1, self.board)
            for square in self.legalmoves:
                self.button_identities[square].configure(background = "red")

            self.board[index-1] = "none"

            photo = tk.PhotoImage(width=1, height=1)

            bname.configure(image = photo)
            bname.image = photo
            #print(self.board)
        else:
            for square in self.legalmoves:
                self.button_identities[square].configure(background = "#f0f0f0")
            
            if index-1 in self.legalmoves:      
                photo = tk.PhotoImage(file= "./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png")
                bname.configure(image = photo)
                bname.image = photo
                self.board[index-1] = self.pickedpiece

                self.pickedpiece = "none"
                #print(self.board)
            else:
                bname = (self.button_identities[self.pickedindex])
                self.board[self.pickedindex] = self.pickedpiece
                photo = tk.PhotoImage(file= "./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png")
                bname.configure(image = photo)
                bname.image = photo

                self.pickedpiece = "none"
        

    def createWidgets(self):   

        for rank in range(0, 8):
            for phile in range(0, 8):

                piece = self.board[rank*8+phile]

                photo = tk.PhotoImage(file = "./sprites/" + piece.color + piece.name + ".png") if piece != "none" else tk.PhotoImage(width=1, height=1)

                x = tk.Button(self, image=photo, height=100, width=100, command = partial(self.recordpress, (rank*8+phile)))
                x.grid(column=phile, row=rank)
                x.image = photo
                self.button_identities.append(x)

app = Application()                       
app.master.title('Sample application')    
app.mainloop()