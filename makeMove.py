from typing import List, Tuple, Union, cast
from Board import Board, BoardState
from Piece import Piece
from FENinterpreter import generateNotation


def makeMove(
    board: Board,
    boardState: BoardState,
    piece: Piece,
    movedTo: int,
    movesList: List[Tuple[Piece, int, int, str]],
    logCheck: bool,
    affectFirstMove: bool = False,
):

    oldBoard: BoardState = boardState[:]

    wasKingsideCastle = False
    wasQueensideCastle = False

    wasEnPassant = False

    if piece.name == "King" and piece.firstmove and abs(piece.position - (movedTo)) == 2:
        eligableRooks = [
            cast(Piece, boardPiece)
            for boardPiece in boardState
            if boardPiece != "none"
            and cast(Piece, boardPiece).name == "Rook"
            and cast(Piece, boardPiece).color == piece.color
            and cast(Piece, boardPiece).firstmove
        ]

        if piece.position > movedTo:
            eligableRook = next((rook for rook in eligableRooks if movedTo > rook.position), None)

            if eligableRook is not None:
                boardState[movedTo + 1] = eligableRook
                boardState[eligableRook.position] = "none"
                eligableRook.position = movedTo + 1
                wasQueensideCastle = True
        else:
            eligableRook = next((rook for rook in eligableRooks if movedTo < rook.position), None)
            if eligableRook is not None:
                boardState[movedTo - 1] = eligableRook
                boardState[eligableRook.position] = "none"
                eligableRook.position = movedTo - 1
                wasKingsideCastle = True

    if piece.name == "Pawn" and not piece.firstmove:
        if movedTo < 8 or movedTo > 55:
            piece.name = "Queen"
        elif (
            piece.color == "White"
            and piece.position != movedTo + 8
            and boardState[movedTo] == "none"
        ):
            boardState[movedTo + 8] = "none"
            wasEnPassant = True

        elif (
            piece.color == "Black"
            and piece.position != movedTo - 8
            and boardState[movedTo] == "none"
        ):
            boardState[movedTo - 8] = "none"
            wasEnPassant = True

    if affectFirstMove:
        piece.firstmove = False

    wasCapture = boardState[movedTo] != "none"

    boardState[piece.position] = "none"
    boardState[movedTo] = piece

    previousLocation = piece.position

    piece.position = movedTo

    setCheck(board, boardState, logCheck)

    if piece.color == "White":
        king = board.whiteKingRef
    else:
        king = board.blackKingRef

    wasCheck = king.inCheck

    differences = [
        (i, boardState[i], oldBoard[i])
        for i in range(len(boardState))
        if oldBoard[i] != boardState[i]
    ]

    notation = generateNotation(
        piece,
        previousLocation,
        movedTo,
        wasCapture,
        wasKingsideCastle,
        wasQueensideCastle,
        wasEnPassant,
        wasCheck and logCheck,
    )

    movesList.append((piece, piece.position, movedTo, notation))

    if logCheck:
        print(notation)

    return differences


def revertMove(
    board: BoardState,
    differences: List[Tuple[int, Union[Piece, str], Union[Piece, str]]],
    movesList: List[Tuple[Piece, int, int, str]],
) -> None:
    for difference in differences:
        index, _, oldPiece = difference
        board[index] = oldPiece
        if oldPiece != "none":
            cast(Piece, oldPiece).position = index

    if len(movesList) > 0:
        movesList.pop()
    return None


def setCheck(board: Board, boardState: BoardState, logCheck: bool) -> None:
    from GenerateLegalMoves import GenerateLegalMovesPreCheck

    whiteKing = board.whiteKingRef

    blackKing = board.blackKingRef

    doubleCheckBlack = 0
    blackKing.inCheck = False
    blackKing.inDoubleCheck = False

    if next(
        (
            boardPiece
            for boardPiece in boardState
            if boardPiece != "none"
            and cast(Piece, boardPiece).color == "White"
            and blackKing.position
            in GenerateLegalMovesPreCheck(cast(Piece, boardPiece).position, boardState, [])
        ),
        None,
    ):
        blackKing.inCheck = True
        doubleCheckBlack += 1
        if logCheck:
            print("Check")

    # if doubleCheckBlack == 2:
    #     blackKing.inDoubleCheck = True
    #     if logCheck:
    #         print("Double Check")
    #     return True

    doubleCheckWhite = 0
    whiteKing.inCheck = False
    whiteKing.inDoubleCheck = False

    if next(
        (
            boardPiece
            for boardPiece in boardState
            if boardPiece != "none"
            and cast(Piece, boardPiece).color == "Black"
            and whiteKing.position
            in GenerateLegalMovesPreCheck(cast(Piece, boardPiece).position, boardState, [])
        ),
        None,
    ):
        whiteKing.inCheck = True
        doubleCheckWhite += 1
        if logCheck:
            print("Check")

    # if doubleCheckWhite == 2:
    #     whiteKing.inDoubleCheck = True
    #     if logCheck:
    #         print("Double Check")
    #     return True


def setCheckMate(board: Board, boardState: BoardState, king: Piece):
    from GenerateLegalMoves import GenerateLegalMoves

    for piece in boardState:
        if piece == "none":
            continue

        piece = cast(Piece, piece)

        if piece.color == king.color:
            legalmoves = GenerateLegalMoves(piece.position, board, boardState, [])
            if len(legalmoves) > 0:
                return

    king.inCheckMate = True
