class Piece:
    name = None
    value = None
    color = None
    position = None
    inplay = None
    namedict = {"r":"Rook", "n":"Knight", "b":"Bishop","q":"Queen","k":"King","p":"Pawn","R":"Rook", "N":"Knight", "B":"Bishop","Q":"Queen","K":"King","P":"Pawn"}
    valuedict = {"Rook": 5, "Knight": 3, "Bishop": 3, "Queen": 9, "Pawn": 1, "King": "N/A"}
    firstmove = True


    def __init__(self, name, position):
        self.name = self.namedict[name]
        self.value = self.valuedict[self.name]
        self.color = "Black" if name.islower() else "White"
        self.position = position
        self.inplay = True
    