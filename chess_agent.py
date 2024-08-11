from mesa import Agent
import chess

class PieceAgent(Agent):
    """Agente base para uma peça de xadrez."""
    def __init__(self, unique_id, model, ai_agent, board, color):
        super().__init__(unique_id, model)
        self.ai_agent = ai_agent
        self.board = board
        self.color = color

    def step(self):
        if not self.board.is_game_over() and self.board.turn == self.color:
            if self.color == chess.WHITE and self.model.controller.player_color == chess.WHITE:
                return
            
            if self.color == chess.BLACK and self.model.controller.player_color == chess.WHITE:
                self.make_move()
                self.model.controller.ai_turn = False

            elif self.color == chess.WHITE and self.model.controller.player_color == chess.BLACK:
                self.make_move()
                self.model.controller.ai_turn = False

    def make_move(self):
        """Método para realizar um movimento, implementado nas subclasses."""
        raise NotImplementedError("Subclasses devem implementar este método.")

class KingAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Rei {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")

class QueenAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Rainha {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")

class RookAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Torre {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")

class BishopAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Bispo {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")

class KnightAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Cavalo {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")

class PawnAgent(PieceAgent):
    def make_move(self):
        move = self.ai_agent.get_move(self.board)
        self.board.push(move)
        print(f"Peão {self.unique_id} ({'Branco' if self.color else 'Preto'}) moveu: {move}")
