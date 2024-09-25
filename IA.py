import random

class IA:
    def __init__(self) -> None:
        pass

    def jogada_ia(self,game, debug_mode, jogador, dificuldade, checar_vitoria, display):
        if dificuldade == 1:  # Nível fácil, IA faz jogadas aleatórias
            while True:
                l, c = self.pos(random.randint(1, 9))
                if game[l][c] == ' ':
                    game[l][c] = jogador
                    break
        else:
            alturamax = 4 if dificuldade == 2 else float('inf')
            l, c = self.melhor_jogada(game, debug_mode, jogador, alturamax, checar_vitoria)
            game[l][c] = jogador
        display.update_buttons(game)
        if checar_vitoria():
            display.status_label.config(text=f"Jogador {jogador} venceu!")
        elif all(cell != ' ' for row in game for cell in row):
            display.status_label.config(text="Deu velha!")
        else:
            display.status_label.config(text="Sua vez!")
    
    def pos(p):
        return (p-1) // 3, (p-1) % 3

    def melhor_jogada(self,game, debug_mode, jogador, alturamax, checar_vitoria):
        best_score = -float('inf')
        move = None
        for l in range(3):
            for c in range(3):
                if game[l][c] == ' ':
                    game[l][c] = jogador
                    score = self.minimax(game, 0, False, debug_mode, jogador, -float('inf'), float('inf'), alturamax, checar_vitoria)
                    game[l][c] = ' '
                    if score > best_score:
                        best_score = score
                        move = (l, c)
        return move
    
    def minimax(self, game, profundidade, is_maximizing, debug_mode, jogador, alpha, beta, alturamax, checar_vitoria):
        score, game_finalizado = self.avaliar(game, profundidade, jogador, checar_vitoria)

        if game_finalizado or profundidade >= alturamax:
            if debug_mode != 3:
                print("Nó folha abaixo, profundidade da arvore: ", profundidade, "Heurística: ", score)
                self.imprimir_tabuleiro(game)
            return score
        elif debug_mode == 1:
            print("Nó percorrido, profundidade da arvore: ", profundidade, "Heurística: ", score)
            self.imprimir_tabuleiro(game)

        if is_maximizing:
            best_score = -float('inf')
            for l in range(3):
                for c in range(3):
                    if game[l][c] == ' ':
                        game[l][c] = jogador
                        score = self.minimax(game, profundidade + 1, False, debug_mode, jogador, alpha, beta, alturamax, checar_vitoria)
                        game[l][c] = ' '
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break  # Poda
            return best_score
        else:
            best_score = float('inf')
            for l in range(3):
                for c in range(3):
                    if game[l][c] == ' ':
                        game[l][c] = 'X' if jogador == 'O' else 'O'
                        score = self.minimax(game, profundidade + 1, True, debug_mode, jogador, alpha, beta, alturamax, checar_vitoria)
                        game[l][c] = ' '
                        best_score = min(best_score, score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break  # Poda
            return best_score

    def avaliar(self,game, profundidade, jogador, checar_vitoria):
        vitorioso = checar_vitoria()

        if vitorioso:
            return (10 - profundidade, True) if vitorioso == jogador else (-20, True)
        elif all(c != ' ' for linha in game for c in linha):
            return 0, True
        
        return 0, False
    
    def imprimir_tabuleiro(self,game):
        for linha in game:
            print(" {} | {} | {} ".format(*linha))
        print()