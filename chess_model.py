from mesa import Model
from mesa.time import RandomActivation
import chess
from chess_agent import KingAgent, QueenAgent, RookAgent, BishopAgent, KnightAgent, PawnAgent

class ChessModel(Model):
    """Modelo que gerencia os agentes de xadrez."""
    def __init__(self, white_ai, black_ai, board):
        self.schedule = RandomActivation(self)
        self.board = board
        
        # Criando agentes para cada tipo de peça
        self.create_agents(white_ai, black_ai)

    def create_agents(self, white_ai, black_ai):
        # Posições iniciais das peças no tabuleiro
        piece_positions = {
            'P': [(chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2),
                  (chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7)],
            'R': [(chess.A1, chess.H1), (chess.A8, chess.H8)],
            'N': [(chess.B1, chess.G1), (chess.B8, chess.G8)],
            'B': [(chess.C1, chess.F1), (chess.C8, chess.F8)],
            'Q': [chess.D1, chess.D8],
            'K': [chess.E1, chess.E8]
        }

        # Adicionando peões
        for idx, pos in enumerate(piece_positions['P'][0]):
            self.schedule.add(PawnAgent(pos, self, white_ai, self.board, chess.WHITE))
        for idx, pos in enumerate(piece_positions['P'][1]):
            self.schedule.add(PawnAgent(pos, self, black_ai, self.board, chess.BLACK))

        # Adicionando Torres
        for idx, pos in enumerate(piece_positions['R'][0]):
            self.schedule.add(RookAgent(pos, self, white_ai, self.board, chess.WHITE))
        for idx, pos in enumerate(piece_positions['R'][1]):
            self.schedule.add(RookAgent(pos, self, black_ai, self.board, chess.BLACK))

        # Adicionando Cavalos
        for idx, pos in enumerate(piece_positions['N'][0]):
            self.schedule.add(KnightAgent(pos, self, white_ai, self.board, chess.WHITE))
        for idx, pos in enumerate(piece_positions['N'][1]):
            self.schedule.add(KnightAgent(pos, self, black_ai, self.board, chess.BLACK))

        # Adicionando Bispos
        for idx, pos in enumerate(piece_positions['B'][0]):
            self.schedule.add(BishopAgent(pos, self, white_ai, self.board, chess.WHITE))
        for idx, pos in enumerate(piece_positions['B'][1]):
            self.schedule.add(BishopAgent(pos, self, black_ai, self.board, chess.BLACK))

        # Adicionando Rainhas
        self.schedule.add(QueenAgent(piece_positions['Q'][0], self, white_ai, self.board, chess.WHITE))
        self.schedule.add(QueenAgent(piece_positions['Q'][1], self, black_ai, self.board, chess.BLACK))

        # Adicionando Reis
        self.schedule.add(KingAgent(piece_positions['K'][0], self, white_ai, self.board, chess.WHITE))
        self.schedule.add(KingAgent(piece_positions['K'][1], self, black_ai, self.board, chess.BLACK))

    def step(self):
        self.schedule.step()
