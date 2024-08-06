import chess_ai
import game_controller

def main():
    ai_agent = chess_ai.ChessAI()
    controller = game_controller.GameController(ai_agent)
    controller.play_game()
    controller.close()

if __name__ == "__main__":
    main()
