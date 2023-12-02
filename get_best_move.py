import chess
import chess.engine


def get_best_move(fen):
    try:
        board = chess.Board(fen=fen)
        engine = chess.engine.SimpleEngine.popen_uci("./stockfish.exe")
        print('Searching best move for this position:')
        best_move = str(engine.play(board, chess.engine.Limit(time=0.1)).move)
        engine.quit()
        return best_move
    except:
        return 'Maybe there is a check'