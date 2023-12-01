import cv2
import numpy as np

template_path = "template.png"
template = cv2.imread(template_path)

template_size = template.shape[0]

line_distance = template_size // 8

for i in range(8):
    for j in range(8):
        # Calculate coordinates of the current cell
        x1, y1 = j * line_distance, i * line_distance
        x2, y2 = (j + 1) * line_distance, (i + 1) * line_distance

        # Extract the current cell from the template
        cell = template[y1:y2, x1:x2]

        # Display the current cell
        cv2.imshow(f"Cell ({i + 1}, {j + 1})", cell)
        cv2.waitKey(0)

cv2.destroyAllWindows()
