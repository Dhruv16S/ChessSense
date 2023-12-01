import cv2
import numpy as np

template_path = "template.png"
template = cv2.imread(template_path)

template_with_lines = template.copy()

template_size = template.shape[0]

line_distance = template_size // 8

for i in range(1, 8):
    x = i * line_distance
    cv2.line(template_with_lines, (x, 0), (x, template_size), (0, 0, 255), 2)  # Red color

for i in range(1, 8):
    y = i * line_distance
    cv2.line(template_with_lines, (0, y), (template_size, y), (0, 0, 255), 2)  # Red color

cv2.imwrite("board_lines.png", template_with_lines)

cv2.imshow("Template with Lines", template_with_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()
