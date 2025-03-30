from typing import List, Tuple, cast
import tkinter as tk
from functools import partial
import re
import time
import threading

from Board import Board
from FENinterpreter import feninterpreter
from GenerateLegalMoves import GenerateLegalMoves
from Piece import Piece
from evaluation import FindMove
from makeMove import makeMove, setCheckMate


class Application(tk.Frame):
    board = Board(feninterpreter("r5k1/5ppp/8/8/8/8/3R1PPP/3R2K1"))
    #board = Board(feninterpreter("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))
    boardState = board.board
    legalmoves = []

    white_time = 0  # seconds
    black_time = 0
    timer_running = False
    timer_label_white: tk.Label
    timer_label_black: tk.Label
    last_tick_time = time.time()

    movelist_label: tk.Label

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

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)  # or tk.Frame.__init__(self, parent)
        self.grid()  # or self.pack() depending on your choice
        self.createWidgets()
        self.gameOver = False
        self.timer_running = True
        self.last_tick_time = time.time()
        self.update_timer()

    def displayGameOver(self, message: str):
        self.gameOver = True

        # Create a message box using a frame-like rectangle
        message_window = tk.Frame(self.board_frame, bg="white", padx=30, pady=20, bd=2, relief="ridge")
        message_window.place(relx=0.5, rely=0.5, anchor="center")

        message_label = tk.Label(
            message_window,
            text=message,
            bg="white",
            fg="black",
            font=("Helvetica", 20, "bold"),
            justify="center",
            wraplength=300
        )
        message_label.pack()

        # Ensure message box is on top
        message_window.lift()


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

            self.legalmoves = GenerateLegalMoves(
                clickedIndex, self.board, self.boardState, self.movesList
            )

            for square in self.legalmoves:
                self.button_identities[square].configure(background="red", activebackground="pink")

            photo = tk.PhotoImage(width=1, height=1)
            pressedButton.configure(image=photo)
            pressedButton.image = photo  # type: ignore

        else:
            self.pickedpiece = cast(Piece, self.pickedpiece)

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
                    self.pickedpiece,
                    clickedIndex,
                    self.movesList,
                    True,
                )

                self.movelist_text.config(state="normal")
                self.movelist_text.delete("1.0", tk.END)
                for i in range(0, len(self.movesList), 2):
                    line = " ".join(move[3] for move in self.movesList[i:i + 2])
                    self.movelist_text.insert(tk.END, line + "\n")
                self.movelist_text.config(state="disabled") 

                for difference in boardDifferences:
                    index, newState, _, _, _ = difference
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

                computer_color = "Black" if self.human_color == "White" else "White"

                if computer_color == "Black":
                    computer_king = self.board.blackKingRef
                else:
                    computer_king = self.board.whiteKingRef

                setCheckMate(self.board, self.boardState, computer_king)

                if computer_king.inCheckMate:
                    self.displayGameOver("Game Over: Checkmate! You Win.")
                    print("Checkmate")

                    for i in range(0, len(self.movesList), 2):
                        print(" ".join(move[3] for move in self.movesList[i : i + 2]))

                self.nextTurn = "Black" if self.nextTurn == "White" else "White"

                if self.nextTurn != self.human_color:
                    self.after(500, lambda: threading.Thread(target=self.computerMove).start())
            else:
                pressedButton = self.button_identities[self.pickedpiece.position]
                self.boardState[self.pickedpiece.position] = self.pickedpiece
                photo = tk.PhotoImage(
                    file="./sprites/" + self.pickedpiece.color + self.pickedpiece.name + ".png"
                )
                pressedButton.configure(image=photo)
                pressedButton.image = photo  # type: ignore

            self.pickedpiece = "none"

    def computerMove(self):
        if self.gameOver:
            return

        computer_color = "Black" if self.human_color == "White" else "White"
        start_time = time.time()
        chosenPiece, chosenDestination, eval = FindMove(
            self.board, self.boardState, computer_color, self.movesList, 2, True
        )

        self.evaluation_value.config(text=str(eval))

        end_time = time.time()
        print(
            f"Time taken to generate legal moves for computer: {(end_time - start_time) * 1000:.2f} milliseconds"
        )

        boardDifferences = makeMove(
            self.board, self.boardState, chosenPiece, chosenDestination, self.movesList, True
        )

        if self.human_color == "Black":
            human_king = self.board.blackKingRef
        else:
            human_king = self.board.whiteKingRef

        setCheckMate(self.board, self.boardState, human_king)

        self.after(0, lambda: self.apply_computer_move(boardDifferences, human_king))

    def apply_computer_move(self, boardDifferences: list[tuple[int, Piece | str, Piece | str, bool, bool]] , human_king: Piece):

        self.movelist_text.config(state="normal")
        self.movelist_text.delete("1.0", tk.END)
        for i in range(0, len(self.movesList), 2):
            line = " ".join(move[3] for move in self.movesList[i:i + 2])
            self.movelist_text.insert(tk.END, line + "\n")
        self.movelist_text.config(state="disabled") 
        
        for difference in boardDifferences:
            index, newState, _, _, _ = difference
            if newState == "none":
                photo = tk.PhotoImage(width=1, height=1)
            else:
                newState = cast(Piece, newState)
                photo = tk.PhotoImage(file="./sprites/" + newState.color + newState.name + ".png")
            visualSquare = self.button_identities[index]
            visualSquare.configure(image=photo)
            visualSquare.image = photo  # type: ignore

        if human_king.inCheckMate:
            self.displayGameOver("Game Over: Checkmate! You Lose.")
            print("Checkmate")
            for i in range(0, len(self.movesList), 2):
                print(" ".join(move[3] for move in self.movesList[i:i + 2]))
            self.timer_running = False
        else:
            self.nextTurn = "Black" if self.nextTurn == "White" else "White"

    def createWidgets(self):
        # Configure grid weight to make layout responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main frame
        self.main_frame = tk.Frame(self, padx=20, pady=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        # Board frame
        self.board_frame = tk.Frame(self.main_frame, bd=2, relief="ridge")
        self.board_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Side panel frame
        self.side_panel_frame = tk.Frame(self.main_frame)
        self.side_panel_frame.grid(row=0, column=1, sticky="n")

        # Chessboard buttons
        for rank in range(8):
            for file in range(8):
                piece = self.boardState[rank * 8 + file]

                if piece == "none":
                    photo = tk.PhotoImage(width=1, height=1)
                else:
                    piece = cast(Piece, piece)
                    photo = tk.PhotoImage(file=f"./sprites/{piece.color}{piece.name}.png")

                btn = tk.Button(
                    self.board_frame,
                    image=photo,
                    height=80,
                    width=80,
                    bg=(self.original_button_light_square_color if (rank + file) % 2 == 0 else self.original_button_dark_square_color),
                    activebackground=self.original_button_active_color,
                    command=partial(self.recordpress, (rank * 8 + file)),
                    name=("lightsquare-" if (rank + file) % 2 == 0 else "darksquare-") + str(rank * 8 + file),
                )
                btn.grid(column=file, row=rank)
                btn.image = photo # type: ignore
                self.button_identities.append(btn)

        # Timer Labels
        label_style = {"font": ("Helvetica", 14), "width": 20, "pady": 10, "border": 1, "relief": "solid"} # type: ignore

        self.timer_label_black = tk.Label(self.side_panel_frame, text="Black Time: 00:00", bg="#333", fg="white", **label_style) # type: ignore
        self.timer_label_black.pack(pady=(0, 10))

        self.timer_label_white = tk.Label(self.side_panel_frame, text="White Time: 00:00", bg="#eee", fg="black", **label_style) # type: ignore
        self.timer_label_white.pack(pady=(0, 20))

        # Move list (Text widget with scrollbar)
        self.movelist_frame = tk.Frame(self.side_panel_frame)
        self.movelist_frame.pack(fill="both", expand=True)

        self.movelist_label = tk.Label(self.movelist_frame, text="Moves", font=("Helvetica", 16, "bold"))
        self.movelist_label.pack(anchor="w")

        self.movelist_text = tk.Text(self.movelist_frame, width=25, height=20, font=("Courier", 12), state="disabled", wrap="none", bd=1, relief="solid")
        self.movelist_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.movelist_frame, command=self.movelist_text.yview) # type: ignore
        self.scrollbar.pack(side="right", fill="y")
        self.movelist_text.config(yscrollcommand=self.scrollbar.set)

        # Evaluation label
        self.evaluation_label = tk.Label(self.side_panel_frame, text="Evaluation: ", font=("Helvetica", 16, "bold"))
        self.evaluation_label.pack(pady=(10, 0))
        self.evaluation_value = tk.Label(self.side_panel_frame, text="0", font=("Helvetica", 16))
        self.evaluation_value.pack(pady=(0, 20))


    def update_timer(self):
        if not self.timer_running:
            return

        now = time.time()
        delta = now - self.last_tick_time
        self.last_tick_time = now

        if self.nextTurn == "White":
            self.white_time += delta
        else:
            self.black_time += delta

        self.timer_label_white.config(text=self.format_time(self.white_time))
        self.timer_label_black.config(text=self.format_time(self.black_time))
        
        if self.gameOver:
            self.timer_running = False
            return
        
        self.after(1000, self.update_timer)

    def format_time(self, seconds: float):
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02}:{secs:02}"


root = tk.Tk()
app = Application(root)  # Application is a tk.Frame
app.grid(row=0, column=0)  # Or pack() — just stay consistent
root.mainloop()