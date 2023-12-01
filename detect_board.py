import cv2
import numpy as np
import pyautogui
import time
import os
import tempfile
from recognize_pieces_positions import recognize_pieces_positions

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

            # Fixing issue of detecting smaller template boards.
            # Chess.com board size for home screen (Tested with Chrome browser) is 750x750.
            if board_width == 750:
                return corners, board_width

    return None, None

while True:
    screenshot = pyautogui.screenshot()
    screen = np.array(screenshot)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    chessboard_corners, board_size = detect_chess_board(screen)
    if chessboard_corners is not None:
        print('Chess board detected.')
        # Extract the region within the chessboard corners
        x, y, w, h = cv2.boundingRect(chessboard_corners)
        chessboard_region = screen[y:y+h, x:x+w]

        chessboard_region_resized = cv2.resize(chessboard_region, (752, 752))
        temp_file_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        cv2.imwrite(temp_file_path, screen)
        recognize_pieces_positions(template_path=temp_file_path,
                                       TOP_OFF=0,
                                       LEFT_OFF=0)
            
        os.remove(temp_file_path)
    else:
        print('Chess board not detected.')
    time.sleep(5)
