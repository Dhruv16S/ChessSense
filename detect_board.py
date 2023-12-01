import cv2
import numpy as np
import pyautogui
import time
import os

CONTOUR_AREA_THRESHOLD = 500

def detect_chess_board(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area to identify the chessboard
    chessboard_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > CONTOUR_AREA_THRESHOLD]

    if chessboard_contours:
        chessboard = max(chessboard_contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(chessboard, True)
        corners = cv2.approxPolyDP(chessboard, epsilon, True)
        corners = corners.reshape(-1, 2)

        if len(corners) != 4:
            return None, None

        # Perform additional checks for lower latency
        top_left, bottom_left, bottom_right, top_right = corners

        top_left_x, top_left_y = top_left
        bottom_left_x, bottom_left_y = bottom_left
        bottom_right_x, bottom_right_y = bottom_right
        top_right_x, top_right_y = top_right

        # Difference of x and y coordinates of the corners should be within 2 pixels
        if abs(top_left_x - bottom_left_x) <= 2 and abs(top_right_x - bottom_right_x) <= 2 and abs(top_left_y - top_right_y) <= 2 and abs(bottom_left_y - bottom_right_y) <= 2:
            if len(os.listdir('./processed')) == 0:
                cv2.imwrite('./processed/gray.jpg', gray)
                cv2.imwrite('./processed/blurred.jpg', blurred)
                cv2.imwrite('./processed/edges.jpg', edges)

            # Compute and verify board size to return it
            board_width = abs(top_left_x - top_right_x)
            board_height = abs(top_left_y - bottom_left_y)
            return corners, board_width

    return None, None

while True:
    screenshot = pyautogui.screenshot()
    screen = np.array(screenshot)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    chessboard_corners, board_size = detect_chess_board(screen)
    if chessboard_corners is not None:
        for i, corner in enumerate(chessboard_corners):
            x, y = corner
            print(f'Chess Board Corner {i + 1}: ({x}, {y})')
        print(f'Board Size: {board_size}')
    else:
        print('Chess board not detected.')
    time.sleep(0.2)
