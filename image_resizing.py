import os
import cv2

board_size = 752
desired_size = (int(board_size/8), int(board_size/8)) 
subfolders = ["black_pieces", "white_pieces"]

for subfolder in subfolders:
    resized_folder_path = f"./resized_pieces/{subfolder}"
    os.makedirs(resized_folder_path, exist_ok=True)
    pieces_folder = f"./pieces/{subfolder}"
    for filename in os.listdir(pieces_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            piece_path = os.path.join(pieces_folder, filename)
            piece_image = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED)
            resized_piece = cv2.resize(piece_image, desired_size)
            resized_piece_path = os.path.join(resized_folder_path, filename)
            cv2.imwrite(resized_piece_path, resized_piece)