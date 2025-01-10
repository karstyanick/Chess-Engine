from typing import Union, Dict

class Piece:
    # Class attributes
    name: Union[str, None]  # The name of the piece (e.g., "Rook", "Pawn")
    value: Union[int, str, None]  # Value of the piece (e.g., 5, 3, "N/A")
    color: Union[str, None]  # The color of the piece ("Black" or "White")
    position: Union[int, None]  # The position of the piece on the board (index 0-63)
    inplay: Union[bool, None]  # Whether the piece is still in play
    namedict: Dict[str, str] = {
        "r": "Rook", "n": "Knight", "b": "Bishop", "q": "Queen", "k": "King", "p": "Pawn",
        "R": "Rook", "N": "Knight", "B": "Bishop", "Q": "Queen", "K": "King", "P": "Pawn"
    }  # Mapping of shorthand to full piece names
    valuedict: Dict[str, Union[int, str]] = {
        "Rook": 5, "Knight": 3, "Bishop": 3, "Queen": 9, "Pawn": 1, "King": "N/A"
    }  # Mapping of full piece names to their values
    firstmove: bool = True  # Whether the piece has moved yet

    # Constructor
    def __init__(self, name: str, position: int):
        self.name: str = self.namedict[name]
        self.value: Union[int, str] = self.valuedict[self.name]
        self.color: str = "Black" if name.islower() else "White"
        self.position: int = position
        self.inplay: bool = True
