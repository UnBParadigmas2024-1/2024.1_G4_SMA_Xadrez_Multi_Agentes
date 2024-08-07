import chess
import chess_logic
import chess_ai
import pygame
import sys

class GameController:
    def __init__(self, ai_agent):
        self.board = chess.Board()
        self.ai_agent = ai_agent
        self.selected_square = None
        self.game_active = True

    def get_square_from_mouse(self, pos):
        """Converte a posição do mouse em um quadrado do tabuleiro de xadrez."""
        x, y = pos
        row, col = y // 100, x // 100
        return chess.square(col, 7 - row)

    def draw_turn_indicator(self, screen):
        """Desenha um indicador para mostrar de quem é a vez de jogar na área do placar."""
        font = pygame.font.SysFont(None, 36)
        if self.board.turn == chess.WHITE:
            turn_text = "Vez da IA"
        else:
            turn_text = "Sua vez"
        turn_surface = font.render(turn_text, True, pygame.Color("black"))
        screen.blit(turn_surface, (810, 10))  # Ajuste a posição conforme necessário

    def draw_scoreboard(self, screen):
        """Desenha o placar ao lado do tabuleiro."""
        pygame.draw.rect(screen, pygame.Color("lightgrey"), pygame.Rect(800, 0, 200, 800))  # Área do placar

        font = pygame.font.SysFont(None, 36)
        # Botão de Reset
        reset_button_rect = pygame.Rect(810, 50, 180, 50)
        pygame.draw.rect(screen, pygame.Color("blue"), reset_button_rect)
        reset_text = font.render("Resetar Jogo", True, pygame.Color("white"))
        screen.blit(reset_text, (825, 60))

        return reset_button_rect

    def draw_selected_square(self, screen):
        """Desenha uma borda preta ao redor do quadrado selecionado."""
        if self.selected_square is not None:
            row, col = divmod(self.selected_square, 8)
            pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(col * 100, (7 - row) * 100, 100, 100), 5)

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Xadrez com SMA")
        clock = pygame.time.Clock()

        while not self.board.is_game_over() and self.game_active:
            screen.fill(pygame.Color("white"))
            chess_logic.draw_board(screen)
            chess_logic.draw_pieces(screen, self.board)
            reset_button_rect = self.draw_scoreboard(screen)
            self.draw_turn_indicator(screen)
            self.draw_selected_square(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if reset_button_rect.collidepoint(pos):
                        self.reset_game()
                    else:
                        clicked_square = self.get_square_from_mouse(pos)
                        print(f"Clicou na posição: {pos}, quadrado: {clicked_square}")

                        if self.board.turn == chess.WHITE:
                            # IA joga como branco
                            print("IA está jogando.")
                            move = self.ai_agent.get_move(self.board)
                            print(f"Movimento da IA: {move}")
                            self.board.push(move)
                        else:
                            # Jogador humano joga
                            piece = self.board.piece_at(clicked_square)
                            if self.selected_square is None:
                                if piece and piece.color == self.board.turn:
                                    self.selected_square = clicked_square
                            else:
                                move = chess.Move(self.selected_square, clicked_square)
                                if move in self.board.legal_moves:
                                    self.board.push(move)
                                    self.selected_square = None
                                    print(f"Movimento realizado: {move}")
                                else:
                                    print("Movimento inválido.")
                                    self.selected_square = None

            # A IA deve jogar no turno dela
            if self.board.turn == chess.WHITE:
                print("IA está jogando automaticamente.")
                move = self.ai_agent.get_move(self.board)
                print(f"Movimento da IA: {move}")
                self.board.push(move)

            clock.tick(60)

        print("Jogo terminado!")
        print("Resultado:", self.board.result())

    def reset_game(self):
        """Reseta o jogo para o estado inicial."""
        self.board = chess.Board()
        self.selected_square = None
        self.game_active = True
        print("Jogo resetado!")

    def close(self):
        self.ai_agent.close()
