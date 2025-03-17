from typing import List, Tuple, Union, cast
from Board import Board
from Piece import Piece


def makeMove(
    board: List[Union[Piece, str]],
    piece: Piece,
    movedTo: int,
    movesList: List[Tuple[Piece, int, int]],
    logCheck: bool,
):

    oldBoard: List[Union[Piece, str]] = board[:]

    if (
        piece.name == "King"
        and piece.firstmove
        and abs(piece.position - (movedTo)) == 2
    ):
        eligableRooks = cast(
            List[Piece],
            [
                piece
                for piece in board
                if piece != "none"
                and cast(Piece, piece).name == "Rook"
                and cast(Piece, piece).color == cast(Piece, piece).color
                and cast(Piece, piece).firstmove
            ],
        )

        if piece.position > movedTo:
            eligableRook = next(
                (rook for rook in eligableRooks if movedTo > rook.position), None
            )
            board[movedTo + 1] = eligableRook
            board[eligableRook.position] = "none"
            eligableRook.position = movedTo + 1
        else:
            eligableRook = next(
                (rook for rook in eligableRooks if movedTo < rook.position), None
            )
            board[movedTo - 1] = eligableRook
            board[eligableRook.position] = "none"
            eligableRook.position = movedTo - 1

    if piece.name == "Pawn" and not piece.firstmove:
        if movedTo < 8 or movedTo > 55:
            piece.name = "Queen"
        elif (
            piece.color == "White"
            and piece.position != movedTo + 8
            and board[movedTo] == "none"
        ):
            board[movedTo + 8] = "none"

        elif (
            piece.position == "Black"
            and piece.position != movedTo - 8
            and board[movedTo] == "none"
        ):
            board[movedTo - 8] = "none"

    wasFirstMove = piece.firstmove
    piece.firstmove = False

    board[piece.position] = "none"
    board[movedTo] = piece

    movesList.append((piece, piece.position, movedTo))
    piece.position = movedTo
    setCheck(board, logCheck)

    differences = [
        (i, board[i], oldBoard[i]) for i in range(len(board)) if oldBoard[i] != board[i]
    ]

    return differences


def revertMove(
    board: Board,
    differences: List[Tuple[int, Union[Piece, str], Union[Piece, str]]],
    movesList: List[Tuple[Piece, int, int]],
) -> None:
    for difference in differences:
        index, _, oldPiece = difference
        board[index] = oldPiece
        if oldPiece != "none":
            oldPiece.position = index

    movesList.pop()
    return None


def setCheck(board: List[Union[Piece, str]], logCheck: bool) -> None:
    from GenerateLegalMoves import GenerateLegalMovesPreCheck

    whiteKing = next(
        (
            boardPiece
            for boardPiece in board
            if boardPiece != "none"
            and boardPiece.name == "King"
            and boardPiece.color == "White"
        ),
        None,
    )
    blackKing = next(
        (
            boardPiece
            for boardPiece in board
            if boardPiece != "none"
            and boardPiece.name == "King"
            and boardPiece.color == "Black"
        ),
        None,
    )

    if blackKing is not None:
        doubleCheckBlack = 0
        blackKing.inCheck = False
        blackKing.inDoubleCheck = False

        if next(
            (
                boardPiece
                for boardPiece in board
                if boardPiece != "none"
                and boardPiece.color == "White"
                and blackKing.position
                in GenerateLegalMovesPreCheck(boardPiece.position, board, [])
            ),
            None,
        ):
            blackKing.inCheck = True
            doubleCheckBlack += 1
            if logCheck:
                print("Check")

        if doubleCheckBlack == 2:
            blackKing.inDoubleCheck = True
            if logCheck:
                print("Double Check")

    if whiteKing is not None:
        doubleCheckWhite = 0
        whiteKing.inCheck = False
        whiteKing.inDoubleCheck = False

        if next(
            (
                boardPiece
                for boardPiece in board
                if boardPiece != "none"
                and boardPiece.color == "Black"
                and whiteKing.position
                in GenerateLegalMovesPreCheck(boardPiece.position, board, [])
            ),
            None,
        ):
            whiteKing.inCheck = True
            doubleCheckWhite += 1
            if logCheck:
                print("Check")

        if doubleCheckWhite == 2:
            whiteKing.inDoubleCheck = True
            if logCheck:
                print("Double Check")

    return None


def setCheckMate(board: List[Union[Piece, str]], king: Piece):
    from GenerateLegalMoves import GenerateLegalMoves

    for piece in board:
        if piece != "none" and piece.color == king.color:
            legalmoves = GenerateLegalMoves(piece.position, board, [])
            if len(legalmoves) > 0:
                return

    king.inCheckMate = True
