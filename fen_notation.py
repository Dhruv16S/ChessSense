class FenNotation:
    choice = None

    def define_choice(self, user_choice):
        FenNotation.choice = user_choice 

    def board_to_fen(self, chessboard):

        # if choice is "black", reverse the board
        if self.choice == 'b':
            chessboard = chessboard[::-1]
            for i in range(len(chessboard)):
                chessboard[i] = chessboard[i][::-1]

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
        if self.choice == 'w':
            fen += " w"
        else:
            fen += " b"
        return fen