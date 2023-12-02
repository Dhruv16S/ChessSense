def board_to_fen(chessboard):
    fen_parts = []
    for row in chessboard:
        fen_row = ''
        empty_count = 0
        for piece in row:
            if piece == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_parts.append(fen_row)

    fen = '/'.join(fen_parts)
    return fen