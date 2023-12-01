import os
import cv2

board_size = 752
desired_size = (int(board_size/8), int(board_size/8)) 

resized_folder_path = "./resized_pieces"
os.makedirs(resized_folder_path, exist_ok=True)

# Iterate through all images in the "pieces" folder
pieces_folder = "./pieces"
for filename in os.listdir(pieces_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Load the piece image
        piece_path = os.path.join(pieces_folder, filename)
        piece_image = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED)

        # Resize the piece image
        resized_piece = cv2.resize(piece_image, desired_size)

        # Save the resized piece in the "resized_pieces" folder
        resized_piece_path = os.path.join(resized_folder_path, filename)
        cv2.imwrite(resized_piece_path, resized_piece)

print("Resizing completed.")
