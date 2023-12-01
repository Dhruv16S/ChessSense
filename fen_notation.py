import chess

def board_to_fen(chessboard):
    board = chess.Board()
    for i, row in enumerate(chessboard):
        for j, piece in enumerate(row):
            if piece != '.':
                square = chess.square(j, 7 - i) 
                board.set_piece_at(square, chess.Piece.from_symbol(piece))

    fen_notation = board.fen()

    return fen_notation