# ChessSense
 ChessSense is a chessboard recognition tool that automates piece detection from images captured from the screen in real-time. With computer vision, it accurately identifies chessboard layouts and piece positions and generates a FEN notation of the current position to recommend the next best move.

## 1. Introduction

For the purposes of this project, all the chess images were taken from [chess.com](https://www.chess.com/), more particularly the Neo pieces and the Green board configuration. Therefore, prior to using the application configure the corresponding settings.

## 2. Project Structure

`./board_templates`: Is the folder that contains all relevant chess board templates used for training and performing image processing tasks.<br>
`./pieces`: Contains two subfolders having the images of the black and white pieces with varying background colours.<br>
`./resized_pieces`: A copy of the above mentioned folder with resized images to perform template matching through image processing and computer vision.<br>
`./thresholds`: Plots to define the colour values and thresholds to distimguish white and black pieces.<br>
`app.py` is the executable application.<br>
`board_lines.py` used to detect the individual cells in a chess board.<br>
`detect_board.py` used to detect the chess board based on the images passed. Performs IP tasks such as countouring and can save intermediate image files in a new folder.<br>
`fen_notation.py` generates the [FEN notation](https://www.chess.com/terms/fen-chess) through the positions of the pieces identified in the chessboard.<br>
`get_best_move.py` predicts the next optimal move by passing the FEN string to a [Stockfish 16](https://stockfishchess.org/) engine.<br>
`image_augmentation.py` and `image_resizing.py` to augment and process images to suitable sizes for image processing.<br>
`recognize_pieces.py` to identify the pieces on a chessboard and their corresponding positions.<br>

## 3. Disclaimer

I have not yet made the application and the corresponding APIs available to the public. The purpose of this project was to use image processing and computer vision to automate the process of playing and learning chess by recommending the best moves. If anyone is willing to access the application, they can do so by following the below steps.

## 4. Installation

1. Clone this repository

```
git clone https://github.com/Dhruv16S/ChessSense.git
```

2. Install required dependencies through

```
pip install -r requirements.txt
```

3. Run the application

```
python app.py
```