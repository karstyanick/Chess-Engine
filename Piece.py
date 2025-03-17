from typing import Dict


class Piece:
    # Class attributes
    namedict: Dict[str, str] = {
        "r": "Rook",
        "n": "Knight",
        "b": "Bishop",
        "q": "Queen",
        "k": "King",
        "p": "Pawn",
        "R": "Rook",
        "N": "Knight",
        "B": "Bishop",
        "Q": "Queen",
        "K": "King",
        "P": "Pawn",
    }  # Mapping of shorthand to full piece names
    valuedict: Dict[str, int] = {
        "Rook": 5,
        "Knight": 3,
        "Bishop": 3,
        "Queen": 9,
        "Pawn": 1,
        "King": 1000,
    }  # Mapping of full piece names to their values
    firstmove: bool = True  # Whether the piece has moved yet
    inCheck: bool = False  # Whether the piece is in check
    inDoubleCheck: bool = False  # Whether the piece is in double check
    inCheckMate: bool = False  # Whether the piece is in checkmate

    color: str  # Color of the piece
    name: str  # Full name of the piece 
    value: int  # Value of the piece
    position: int  # Position of the piece
    inplay: bool  # Whether the piece

    # Constructor
    def __init__(self, name: str, position: int):
        self.name: str = self.namedict[name]
        self.value: int = self.valuedict[self.name]
        self.color: str = "Black" if name.islower() else "White"
        self.position: int = position
        self.inplay: bool = True
