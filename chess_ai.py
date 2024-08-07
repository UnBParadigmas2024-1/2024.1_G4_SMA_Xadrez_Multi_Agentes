import chess
import chess.engine
import os

class ChessAI:
    def __init__(self):
        self.stockfish_path = self.get_stockfish_path()
        self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

    def get_stockfish_path(self):
        system = os.name
        if system == 'nt':
            return "./stockfish_windows/stockfish-windows-x86-64.exe"
        elif os.uname().sysname == 'Darwin':
            return "./stockfish_mac/stockfish-macos-x86-64"
        elif system == 'posix':
            return "stockfish_ubuntu/stockfish-ubuntu-x86-64-avx2"
        else:
            raise Exception("Sistema operacional não suportado")

    def get_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.7))
        return result.move

    def close(self):
        self.engine.quit()
