import cv2
import os
import numpy as np

def replace_color(image_path, original_color, new_color):
    image = cv2.imread(image_path)
    lower_bound = np.array(original_color, dtype=np.uint8)
    upper_bound = np.array(original_color, dtype=np.uint8)
    mask = cv2.inRange(image, lower_bound, upper_bound)
    image[np.where(mask > 0)] = new_color
    filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(os.path.dirname(image_path), f"{filename}_white_bg.png")
    cv2.imwrite(output_path, image)
    print(f"Image saved: {output_path}")

input_folder = "pieces"
subfolders = ["black_pieces", "white_pieces"]

# Chess.com Neo Board
white_color = [204, 237, 233]  # Color #e9edcc
black_color = [84, 153, 84]    # Color #779954

for subfolder in subfolders:
    input_folder = os.path.join("pieces", subfolder)
    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)
            print(image_path)
            replace_color(image_path, black_color, white_color)