# Same logic as recognize_pieces_positions.py, but is used to define thresholds

import cv2
import numpy as np
import os
import time
import matplotlib.pyplot as plt

def extract_prominent_colors(cell):
    flattened_cell = cell.reshape((-1, 3))
    k = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(np.float32(flattened_cell), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    prominent_colors = np.uint8(centers)
    return np.mean(np.abs(prominent_colors[0] - prominent_colors[1]))

def define_thresholds(template_path, LEFT_OFF, TOP_OFF, start, end, step):

    mean_absolute_color_differences = []
    mean_absolute_color_differences_pieces = [] 

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
        # (7, 5, -1) for white pieces
        # (0, 2, 1) for black pieces
        for i in range(start, end, step):
            for j in range(8):
                x1, y1 = j * line_distance + LEFT_OFF, i * line_distance + TOP_OFF
                x2, y2 = (j + 1) * line_distance  + LEFT_OFF, (i + 1) * line_distance  + TOP_OFF

                cell = template[y1:y2, x1:x2]
                if cell.shape[0] != line_distance:
                    continue
                pieces_folder = f"./resized_pieces/{subfolder}"

                piece_names = []
                confidence_scores = []

                for piece_file in os.listdir(pieces_folder):
                    if piece_file.endswith(".png"):
                        piece_path = os.path.join(pieces_folder, piece_file)
                        piece = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED) 
                        
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
                    mean_absolute_color_differences.append(extract_prominent_colors(cell))
                    mean_absolute_color_differences_pieces.append(final_piece_name.replace(".png", ""))
                    final_piece_name = final_piece_name.replace(".png", "").replace("_white_bg", "").replace("_played_move", "")
                    chessboard[i][j] = piece_and_symbol[final_piece_name]
    return mean_absolute_color_differences, mean_absolute_color_differences_pieces

white_piece_threshold, piece_names = define_thresholds(template_path="./templates/template.png", LEFT_OFF=0, TOP_OFF=0, start=7, end=5, step=-1)
plt.scatter(piece_names, white_piece_threshold, marker='o')
plt.title('Mean Absolute Color Difference for White Pieces')
plt.xlabel('Piece Name', fontsize=10)
plt.ylabel('Mean Absolute Color Difference', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('./thresholds/white_pieces.png', bbox_inches='tight')
plt.clf()

played_white_piece_threshold, piece_names = define_thresholds(template_path="./templates/template_4.png", LEFT_OFF=0, TOP_OFF=0, start=1, end=2, step=1)
print(played_white_piece_threshold)
plt.scatter(piece_names, played_white_piece_threshold, marker='o')
plt.title('Mean Absolute Color Difference for Played White Pieces')
plt.xlabel('Piece Name', fontsize=10)
plt.ylabel('Mean Absolute Color Difference', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('./thresholds/played_white_pieces.png', bbox_inches='tight')
plt.clf()

black_piece_threshold, piece_names = define_thresholds(template_path="./templates/template.png", LEFT_OFF=0, TOP_OFF=0, start=0, end=2, step=1)
plt.scatter(piece_names, black_piece_threshold, marker='o')
plt.title('Mean Absolute Color Difference for Black Pieces')
plt.xlabel('Piece Name', fontsize=10)
plt.ylabel('Mean Absolute Color Difference', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('./thresholds/black_pieces.png', bbox_inches='tight')
plt.clf()

played_black_piece_threshold, piece_names = define_thresholds(template_path="./templates/template_3.png", LEFT_OFF=0, TOP_OFF=0, start=3, end=4, step=1)
plt.scatter(piece_names, played_black_piece_threshold, marker='o')
plt.title('Mean Absolute Color Difference for Played Black Pieces')
plt.xlabel('Piece Name', fontsize=10)
plt.ylabel('Mean Absolute Color Difference', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('./thresholds/played_black_pieces.png', bbox_inches='tight')
plt.clf()

empty_threshold, empty_name = define_thresholds(template_path="./templates/template.png", LEFT_OFF=0, TOP_OFF=0, start=2, end=3, step=1)
plt.scatter(empty_name, empty_threshold, marker='o')
plt.title('Mean Absolute Color Difference for Empty Cells')
plt.xlabel('Empty Cell', fontsize=10)
plt.ylabel('Mean Absolute Color Difference', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('./thresholds/empty_cells.png', bbox_inches='tight')
plt.clf()