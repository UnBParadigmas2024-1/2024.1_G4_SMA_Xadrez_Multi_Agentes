import chess
import chess.engine
import os
import random

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

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def get_move(self, board):
        time_limit = 0.7 
        if self.difficulty == 'easy':
            time_limit = 0.1 
        elif self.difficulty == 'medium':
            time_limit = 0.7  # Tempo médio (padrão)
        elif self.difficulty == 'hard':
            time_limit = 1.5 

        legal_moves = list(board.legal_moves)

        if self.difficulty == 'easy':
            # Add randomness: 50% chance to make a random legal move
            if random.random() < 0.5:
                return random.choice(legal_moves)
        if self.difficulty == 'medium':
            # Add randomness: 30% chance to make a random legal move
            if random.random() < 0.3:
                return random.choice(legal_moves)
        if self.difficulty == 'hard':
            # Add randomness: 10% chance to make a random legal move
            if random.random() < 0.1:
                return random.choice(legal_moves)
        
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move

    def close(self):
        self.engine.quit()
