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
        self.ai_turn = False  # Inicialmente, é a vez do jogador (brancas)
        self.difficulty = 'medium'  # Dificuldade padrão
    
    def display_difficulty_menu(self, screen):
        """Exibe um menu para o jogador escolher a dificuldade."""
        screen.fill(pygame.Color("white"))
        font = pygame.font.SysFont(None, 60)
        difficulties = ['Easy', 'Medium', 'Hard']
        buttons = []

        for i, diff in enumerate(difficulties):
            text = font.render(diff, True, pygame.Color("black"))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 100))
            button_rect = pygame.Rect(
                text_rect.left - 20, text_rect.top - 10, text_rect.width + 40, text_rect.height + 20
            )
            pygame.draw.rect(screen, pygame.Color("lightblue"), button_rect)
            pygame.draw.rect(screen, pygame.Color("blue"), button_rect, 2)  # Outline
            screen.blit(text, text_rect)
            buttons.append((button_rect, diff))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button_rect, diff in buttons:
                        if button_rect.collidepoint(pos):
                            self.difficulty = diff.lower()
                            return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.difficulty = 'easy'
                        return
                    elif event.key == pygame.K_2:
                        self.difficulty = 'medium'
                        return
                    elif event.key == pygame.K_3:
                        self.difficulty = 'hard'
                        return

    def set_difficulty(self, difficulty):
        """Ajusta a dificuldade da IA."""
        if difficulty == 'easy':
            self.time_limit = 0.1  # Menor tempo para movimentos mais fáceis
        elif difficulty == 'medium':
            self.time_limit = 0.7  # Tempo padrão
        elif difficulty == 'hard':
            self.time_limit = 2.0  # Mais tempo para movimentos mais difíceis
        else:
            raise ValueError("Nível de dificuldade desconhecido")

    def get_square_from_mouse(self, pos, start_x, start_y):
        """Converte a posição do mouse em um quadrado do tabuleiro de xadrez."""
        x, y = pos
        if start_x <= x < start_x + 800 and start_y <= y < start_y + 800:
            row, col = (y - start_y) // 100, (x - start_x) // 100
            return chess.square(col, 7 - row)
        return None

    def draw_turn_indicator(self, screen, start_x, start_y):
        """Desenha um indicador para mostrar de quem é a vez de jogar na área do placar."""
        font = pygame.font.SysFont(None, 36)
        if self.ai_turn:
            turn_text = "Vez da IA"
        else:
            turn_text = "Sua vez"
        turn_surface = font.render(turn_text, True, pygame.Color("black"))
        screen.blit(turn_surface, (start_x + 810, start_y + 10))  # Ajuste a posição conforme necessário

    def draw_scoreboard(self, screen, start_x, start_y):
        """Desenha o placar ao lado do tabuleiro."""
        board_width = 800  # Largura do tabuleiro
        scoreboard_width = 200
        scoreboard_height = 800  # Altura do placar (igual à altura do tabuleiro)

        # Calcula a posição do placar
        scoreboard_x = start_x + board_width
        scoreboard_y = start_y

        # Desenha a área do placar
        pygame.draw.rect(screen, pygame.Color("lightgrey"), pygame.Rect(scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height))

        font = pygame.font.SysFont(None, 36)

        # Botão de Reset
        reset_button_width = 180
        reset_button_height = 50
        reset_button_x = scoreboard_x + (scoreboard_width - reset_button_width) // 2
        reset_button_y = start_y + 50
        reset_button_rect = pygame.Rect(reset_button_x, reset_button_y, reset_button_width, reset_button_height)
        
        pygame.draw.rect(screen, pygame.Color("blue"), reset_button_rect)
        reset_text = font.render("Resetar Jogo", True, pygame.Color("white"))
        text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, text_rect)

        # Botão de Alterar Dificuldade
        change_difficulty_button_y = reset_button_y + 70  # Adjust as needed
        change_difficulty_button_rect = pygame.Rect(reset_button_x, change_difficulty_button_y, reset_button_width, reset_button_height)
        
        pygame.draw.rect(screen, pygame.Color("blue"), change_difficulty_button_rect)
        change_difficulty_text = font.render("Alterar Dificuldade", True, pygame.Color("white"))
        change_difficulty_text_rect = change_difficulty_text.get_rect(center=change_difficulty_button_rect.center)
        screen.blit(change_difficulty_text, change_difficulty_text_rect)

        # Botão de Desfazer Movimento
        undo_button_y = change_difficulty_button_y + 70  # Ajuste conforme necessário
        undo_button_rect = pygame.Rect(reset_button_x, undo_button_y, reset_button_width, reset_button_height)

        pygame.draw.rect(screen, pygame.Color("blue"), undo_button_rect)
        undo_text = font.render("Desfazer Movimento", True, pygame.Color("white"))
        undo_text_rect = undo_text.get_rect(center=undo_button_rect.center)
        screen.blit(undo_text, undo_text_rect)

        # Retornar todos os retângulos de botão para verificações de clique
        return reset_button_rect, change_difficulty_button_rect, undo_button_rect

    def draw_selected_square(self, screen, start_x, start_y):
        """Desenha uma borda preta ao redor do quadrado selecionado."""
        if self.selected_square is not None:
            row, col = divmod(self.selected_square, 8)
            pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(start_x + col * 100, start_y + (7 - row) * 100, 100, 100), 5)

    def calculate_board_start_position(self, screen_width, screen_height):
        board_size = min(screen_width - 200, screen_height)  # Ajuste o tamanho do tabuleiro com base na menor dimensão disponível
        start_x = (screen_width - board_size - 200) // 2  # Subtrai a largura do placar
        start_y = (screen_height - board_size) // 2
        return start_x, start_y, board_size

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Xadrez com SMA")
        clock = pygame.time.Clock()

        self.display_difficulty_menu(screen)
        self.ai_agent.set_difficulty(self.difficulty)
        self.game_active = True

        while not self.board.is_game_over() and self.game_active:
            screen_width, screen_height = screen.get_size()
            start_x, start_y, board_size = self.calculate_board_start_position(screen_width, screen_height)

            screen.fill(pygame.Color("white"))
            chess_logic.draw_board(screen, start_x, start_y)
            chess_logic.draw_pieces(screen, self.board, start_x, start_y)
            reset_button_rect, change_difficulty_button_rect, undo_button_rect = self.draw_scoreboard(screen, start_x, start_y)
            self.draw_turn_indicator(screen, start_x, start_y)
            self.draw_selected_square(screen, start_x, start_y)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if reset_button_rect.collidepoint(pos):
                        self.reset_game()
                    elif change_difficulty_button_rect.collidepoint(pos):
                        self.display_difficulty_menu(screen)
                        self.ai_agent.set_difficulty(self.difficulty)
                    elif undo_button_rect.collidepoint(pos):
                        self.undo_move()  # Chama a função de desfazer movimento
                    else:
                        clicked_square = self.get_square_from_mouse(pos, start_x, start_y)
                        if clicked_square is not None:
                            print(f"Clicou na posição: {pos}, quadrado: {clicked_square}")

                        if not self.ai_turn:
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
                                    self.ai_turn = True  # Após o movimento do jogador, é a vez da IA
                                else:
                                    print("Movimento inválido.")
                                    self.selected_square = None

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.w, event.h
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            # A IA deve jogar no turno dela
            if self.ai_turn and not self.board.is_game_over():
                print("IA está jogando automaticamente.")
                move = self.ai_agent.get_move(self.board)
                print(f"Movimento da IA: {move}")
                self.board.push(move)
                self.ai_turn = False  # Após o movimento da IA, é a vez do jogador

            clock.tick(60)

        print("Jogo terminado!")
        print("Resultado:", self.board.result())

    def reset_game(self):
        """Reseta o jogo para o estado inicial."""
        self.board = chess.Board()
        self.selected_square = None
        self.game_active = True
        self.ai_turn = False  # Jogador começa com as peças brancas
        print("Jogo resetado!")

    def undo_move(self):
        """Desfaz os últimos dois movimentos realizados (jogador e IA)."""
        moves_to_undo = 2  # Desfaz dois movimentos

        while moves_to_undo > 0 and len(self.board.move_stack) > 0:
            self.board.pop()  # Desfaz um movimento
            moves_to_undo -= 1

        # Atualiza o turno do jogador para que ele possa jogar novamente
        self.ai_turn = False

        if moves_to_undo == 0:
            print("Dois movimentos desfeitos!")
        else:
            print("Não há movimentos suficientes para desfazer.")

        # Atualiza o tabuleiro na tela
        screen_width, screen_height = pygame.display.get_surface().get_size()
        start_x, start_y, board_size = self.calculate_board_start_position(screen_width, screen_height)

        screen = pygame.display.get_surface()
        screen.fill(pygame.Color("white"))
        chess_logic.draw_board(screen, start_x, start_y)
        chess_logic.draw_pieces(screen, self.board, start_x, start_y)
        self.draw_scoreboard(screen, start_x, start_y)
        self.draw_turn_indicator(screen, start_x, start_y)
        self.draw_selected_square(screen, start_x, start_y)
        pygame.display.flip()


    def close(self):
        self.ai_agent.close()
        pygame.quit()
        sys.exit()
