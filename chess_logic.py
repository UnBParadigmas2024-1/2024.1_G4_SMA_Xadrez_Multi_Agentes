import pygame
import chess

def draw_board(screen, start_x, start_y):
    """Desenha o tabuleiro de xadrez e as coordenadas."""
    colors = [pygame.Color("white"), pygame.Color("gray")]
    font = pygame.font.SysFont(None, 18)  # Fonte menor para o texto das coordenadas

    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(start_x + c * 100, start_y + r * 100, 100, 100))
            
            # Desenhe as coordenadas no canto inferior direito de cada quadrado
            coord_text = f"{chr(65 + c)}{8 - r}"  # Calcula a coordenada (ex: A1, B1, etc.)
            text_surface = font.render(coord_text, True, pygame.Color("black"))
            text_rect = text_surface.get_rect(bottomright=(start_x + c * 100 + 95, start_y + r * 100 + 95))
            screen.blit(text_surface, text_rect)

def draw_pieces(screen, board, start_x, start_y):
    """Desenha as peças no tabuleiro."""
    piece_images = {
        "P": pygame.image.load("images/wp.png"),
        "R": pygame.image.load("images/wr.png"),
        "N": pygame.image.load("images/wn.png"),
        "B": pygame.image.load("images/wb.png"),
        "Q": pygame.image.load("images/wq.png"),
        "K": pygame.image.load("images/wk.png"),
        "p": pygame.image.load("images/bp.png"),
        "r": pygame.image.load("images/br.png"),
        "n": pygame.image.load("images/bn.png"),
        "b": pygame.image.load("images/bb.png"),
        "q": pygame.image.load("images/bq.png"),
        "k": pygame.image.load("images/bk.png")
    }

    piece_size = 60  # 25% menor que 100 (tamanho original do quadrado)
    margin = 12.5    # Margem para centralizar a peça dentro do quadrado

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = piece_images[str(piece)]
            piece_image = pygame.transform.scale(piece_image, (piece_size, piece_size))
            row, col = divmod(square, 8)
            x = start_x + col * 100 + margin
            y = start_y + (7 - row) * 100 + margin
            screen.blit(piece_image, pygame.Rect(x, y, piece_size, piece_size))


