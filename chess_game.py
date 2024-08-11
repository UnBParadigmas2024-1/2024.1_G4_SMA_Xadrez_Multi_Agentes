import chess_ai
import game_controller

def main():
    white_ai = chess_ai.ChessAI()
    black_ai = chess_ai.ChessAI()
    controller = game_controller.GameController(white_ai, black_ai)
    controller.play_game()
    controller.close()

if __name__ == "__main__":
    main()
