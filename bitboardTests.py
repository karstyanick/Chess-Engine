import pygame
import sys

# Constants
BOARD_SIZE = 8  # Chessboard is 8x8
TILE_SIZE = 80  # Size of each square in pixels
WINDOW_SIZE = BOARD_SIZE * TILE_SIZE  # Total window size
SPRITE_FOLDER = "sprites"  # Folder containing piece images

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Board")

LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)

# Pieces dictionary
pieces = {
    "white": {
        "pawns": 0b0,
        "rooks": 0b0,
        "knights": 0b0,
        "bishops": 0b0,
        "queens": 0b0,
        "king": 0b0
    },
    "black": {
        "pawns": 0b0,
        "rooks": 0b0,
        "knights": 0b0,
        "bishops": 0b0,
        "queens": 0b0,
        "king": 0b0
    }
}

# Function to initialize the starting position
def startingPosition():
    pieces["black"]["pawns"] = 0b0000000000000000000000000000000000000000000000001111111100000000
    pieces["black"]["rooks"] = 0b0000000000000000000000000000000000000000000000000000000010000001
    pieces["black"]["knights"] = 0b0000000000000000000000000000000000000000000000000000000001000010
    pieces["black"]["bishops"] = 0b0000000000000000000000000000000000000000000000000000000000100100
    pieces["black"]["queens"] = 0b0000000000000000000000000000000000000000000000000000000000001000
    pieces["black"]["king"] = 0b0000000000000000000000000000000000000000000000000000000000010000

    pieces["white"]["pawns"] = 0b0000000011111111000000000000000000000000000000000000000000000000
    pieces["white"]["rooks"] = 0b1000000100000000000000000000000000000000000000000000000000000000
    pieces["white"]["knights"] = 0b0100001000000000000000000000000000000000000000000000000000000000
    pieces["white"]["bishops"] = 0b0010010000000000000000000000000000000000000000000000000000000000
    pieces["white"]["queens"] = 0b0000100000000000000000000000000000000000000000000000000000000000
    pieces["white"]["king"] = 0b0001000000000000000000000000000000000000000000000000000000000000

# Draw the chessboard
def drawBoard():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Draw a specific type of piece based on a bitboard
def drawPieceType(bitboard, sprite_path):
    sprite = pygame.image.load(sprite_path)
    sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
    
    for square in range(64):  # Loop through all 64 squares
        if bitboard & (1 << square):  # If this square contains the piece
            row = square // BOARD_SIZE
            col = square % BOARD_SIZE
            screen.blit(sprite, (col * TILE_SIZE, row * TILE_SIZE))

# Function to draw all pieces
def drawAllPieces():
    for color in pieces:
        for piece, bitboard in pieces[color].items():
            piece_name = piece.capitalize()

            if piece != "king":
                piece_name = piece_name[:-1]
            
            sprite_path = f"{SPRITE_FOLDER}/{color.capitalize()}{piece_name}.png"
            drawPieceType(bitboard, sprite_path)


def movePawn(square, direction):
    """
    Move a specific pawn forward if the move is valid.

    :param pawns: Bitboard of pawns
    :param occupied_squares: Bitboard of all occupied squares
    :param square: The current square index of the pawn (0 to 63)
    :param direction: 8 for white pawns (shift left), -8 for black pawns (shift right)
    :return: Updated bitboard of pawns
    """
    specific_pawn = 1 << square  # Create a bitmask for the specific pawn

    # Check if the specific pawn exists in the bitboard
    if pieces["white"]["pawns"] & specific_pawn == 0:
        raise ValueError("No pawn at the specified square")

    # Move the specific pawn
    if direction == 8:  # White pawn
        new_position = specific_pawn << 8
    elif direction == -8:  # Black pawn
        new_position = specific_pawn >> 8
    else:
        raise ValueError("Invalid direction. Use 8 for white or -8 for black.")

    # Update the pawns bitboard
    pieces["white"]["pawns"] &= ~specific_pawn  # Remove the pawn from its current position
    pieces["white"]["pawns"] |= new_position    # Add the pawn to its new position


# Main function
def main():
    startingPosition()
    clock = pygame.time.Clock()  # Create a clock object

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the board and pieces
        drawBoard()
        drawAllPieces()

        # Update the display
        pygame.display.flip()

        clock.tick(0.5)

        movePawn(52, -8)

# Run the game
if __name__ == "__main__":
    main()