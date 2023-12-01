import cv2
import numpy as np
import os

template_path = "template.png"
template = cv2.imread(template_path)

template_size = template.shape[0]

line_distance = template_size // 8

for i in range(8):
    for j in range(8):
        x1, y1 = j * line_distance, i * line_distance
        x2, y2 = (j + 1) * line_distance, (i + 1) * line_distance

        cell = template[y1:y2, x1:x2]

        pieces_folder = "./resized_pieces"
        for piece_file in os.listdir(pieces_folder):
            if piece_file.endswith(".png"):
                piece_path = os.path.join(pieces_folder, piece_file)
                piece = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED)
                
                if piece.shape[2] == 4:
                    piece = cv2.cvtColor(piece, cv2.COLOR_BGRA2BGR)

                piece = cv2.resize(piece, (cell.shape[1], cell.shape[0]))

                result = cv2.matchTemplate(cell, piece, cv2.TM_CCOEFF_NORMED)

                threshold = 0.8  

                locations = np.where(result >= threshold)

                for loc in zip(*locations[::-1]):
                    top_left = (x1 + loc[0], y1 + loc[1])
                    bottom_right = (top_left[0] + piece.shape[1], top_left[1] + piece.shape[0])
                    cv2.rectangle(template, top_left, bottom_right, (0, 0, 255), 2)

                    # Print the position of the detected piece in the cell
                    print(f"  Piece {piece_file}: ({top_left[0]}, {top_left[1]}) to ({bottom_right[0]}, {bottom_right[1]})")

# Display the template image with bounding boxes
cv2.imshow("Template with Bounding Boxes", template)
cv2.waitKey(0)
cv2.destroyAllWindows()
