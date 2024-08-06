import chess_ai
import game_controller

def main():
    # Inicializa o agente de IA
    ai_agent = chess_ai.ChessAI()
    
    # Inicializa o controlador de jogo com o agente de IA
    controller = game_controller.GameController(ai_agent)
    
    # Inicia o jogo
    controller.play_game()
    
    # Fecha o agente de IA após o jogo
    controller.close()

if __name__ == "__main__":
    main()
