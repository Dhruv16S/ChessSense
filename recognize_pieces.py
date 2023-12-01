import cv2
import numpy as np

# Constants
BOARD_SIZE = 750
CELL_SIZE = BOARD_SIZE // 8
BOARD_TOP_COORD = 0  # Change this based on your actual top coordinate
BOARD_LEFT_COORD = 0  # Change this based on your actual left coordinate
CONFIDENCE = 0
DETECTION_NOISE_THRESHOLD = 8
PIECES_PATH = './pieces/'

# Piece names to FEN characters mapping
piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}

# Get coordinates of chess pieces
def recognize_position(board_image):
    piece_locations = {piece: [] for piece in piece_names.keys()}

    for piece in piece_names.keys():
        template = cv2.imread(PIECES_PATH + piece + '.png', cv2.IMREAD_UNCHANGED)

        # Extract alpha channel
        alpha_channel = template[:, :, 3]

        # Set alpha channel to 1 for non-transparent pixels
        template[:, :, 3] = np.where(alpha_channel > 0, 1, 0)

        result = cv2.matchTemplate(board_image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= CONFIDENCE)

        for loc in zip(*locations[::-1]):
            piece_locations[piece].append(loc)

    return piece_locations

# Convert piece coordinates to 2D list
def locations_to_board(piece_locations):
    chess_board = [['.' for _ in range(8)] for _ in range(8)]

    for row in range(8):
        for col in range(8):
            x = BOARD_LEFT_COORD + col * CELL_SIZE
            y = BOARD_TOP_COORD + row * CELL_SIZE

            for piece_type, locations in piece_locations.items():
                for loc in locations:
                    if abs(loc[0] - x) < DETECTION_NOISE_THRESHOLD and \
                       abs(loc[1] - y) < DETECTION_NOISE_THRESHOLD:
                        chess_board[row][col] = piece_names[piece_type]

    return chess_board

# Read chessboard image from file
board_image = cv2.imread('template.png', cv2.IMREAD_UNCHANGED)

while True:
    try:
        piece_locations = recognize_position(board_image)
        chess_board = locations_to_board(piece_locations)

        # Print the chess board
        for row in chess_board:
            print(" ".join(row))

    except KeyboardInterrupt:
        break
