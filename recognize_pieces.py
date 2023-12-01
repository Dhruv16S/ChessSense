import cv2
import numpy as np
import os
from fen_notation import board_to_fen

template_path = "template.png"
template = cv2.imread(template_path)

template_size = template.shape[0]

line_distance = template_size // 8

subfolders = ["white_pieces", "black_pieces"]

# 0 for white, 1 for black
# If the play is from black's perspective, invert the board and change this to 1
current_move = 0

chessboard = [["." for i in range(8)] for j in range(8)]

piece_and_symbol = {
    "white_pawn" : "P",
    "white_knight" : "N",
    "white_bishop" : "B",
    "white_rook" : "R",
    "white_queen" : "Q",
    "white_king" : "K",
    "black_pawn" : "p",
    "black_knight" : "n",
    "black_bishop" : "b",
    "black_rook" : "r",
    "black_queen" : "q",
    "black_king" : "k"
}

for subfolder in subfolders:
    for i in range(8):
        for j in range(8):
            x1, y1 = j * line_distance, i * line_distance
            x2, y2 = (j + 1) * line_distance, (i + 1) * line_distance

            cell = template[y1:y2, x1:x2]

            # pieces_folder = f"./resized_pieces/{subfolders[current_move]}"
            pieces_folder = f"./resized_pieces/{subfolder}"

            # Maybe use a dictionary instead of two lists
            piece_names = []
            confidence_scores = []

            for piece_file in os.listdir(pieces_folder):
                if piece_file.endswith(".png"):
                    piece_path = os.path.join(pieces_folder, piece_file)
                    piece = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED) 
                    
                    # Resize the piece image to match the cell size
                    piece = cv2.resize(piece, (cell.shape[1], cell.shape[0]))

                    result = cv2.matchTemplate(cell, piece, cv2.TM_CCOEFF_NORMED)

                    threshold = 0.53

                    locations = np.where(result >= threshold)

                    for loc in zip(*locations[::-1]):
                        piece_names.append(piece_file)
                        confidence_scores.append(result[loc[1], loc[0]])
                        break 
            if len(confidence_scores) != 0:
                final_piece_name = piece_names[confidence_scores.index(max(confidence_scores))]
                final_piece_name = final_piece_name.replace(".png", "").replace("_white_bg", "")
                chessboard[i][j] = piece_and_symbol[final_piece_name]

fen_notation = board_to_fen(chessboard)
print(fen_notation)