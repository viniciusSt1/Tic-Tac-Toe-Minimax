import random

def imprimir_tabuleiro(game):
    for linha in game:
        print(" {} | {} | {} ".format(*linha))
    print()

def posicao_valida(game, p):
    if p < 1 or p > 9:
        return False
    l, c = pos(p)
    return game[l][c] == ' '

def pos(p):
    return (p-1) // 3, (p-1) % 3

def checar_vitoria(game):
    for i in range(3):
        if game[i][0] == game[i][1] == game[i][2] != ' ':
            return game[i][0]
        if game[0][i] == game[1][i] == game[2][i] != ' ':
            return game[0][i]
    
    if game[0][0] == game[1][1] == game[2][2] != ' ':
        return game[0][0]
    if game[2][0] == game[1][1] == game[0][2] != ' ':
        return game[2][0]
    
    return False

def avaliar(game, profundidade, jogador):
    vitorioso = checar_vitoria(game)

    if vitorioso:
        return (10 - profundidade, True) if vitorioso == jogador else (-20, True)
    elif all(c != ' ' for linha in game for c in linha):
        return 0, True
    
    return 0, False #Jogo não finalizado, atribuindo heurística de jogo empatado

def minimax(game, profundidade, is_maximizing, debug_mode, jogador, alpha, beta, alturamax):
    score, game_finalizado = avaliar(game, profundidade, jogador)

    if game_finalizado or profundidade >= alturamax:
        if debug_mode != 3:  
            print("Nó folha abaixo, profundidade atual da árvore:  ", profundidade, " Heurística: ", score, "\n")
            imprimir_tabuleiro(game)
        return score

    if is_maximizing:
        best_score = -float('inf')
        for l in range(3):
            for c in range(3):
                if game[l][c] == ' ':
                    game[l][c] = jogador
                    score = minimax(game, profundidade + 1, False, debug_mode, jogador, alpha, beta, alturamax)
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
                    score = minimax(game, profundidade + 1, True, debug_mode, jogador, alpha, beta, alturamax)
                    game[l][c] = ' '
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break  # Poda
        return best_score

def melhor_jogada(game, debug_mode, jogador, alturamax):
    best_score = -float('inf')
    move = None
    for l in range(3):
        for c in range(3):
            if game[l][c] == ' ':
                game[l][c] = jogador
                score = minimax(game, 0, False, debug_mode, jogador, -float('inf'), float('inf'), alturamax)
                game[l][c] = ' '
                if score > best_score:
                    best_score = score
                    move = (l, c)
    return move

def jogada_ia(game, debug_mode, jogador, dificuldade):
    if dificuldade == 1:  # Nível fácil, IA faz jogadas aleatórias
        while True:
            l, c = pos(random.randint(1, 9))
            if game[l][c] == ' ':
                game[l][c] = jogador
                break
    else:
        alturamax = 4 if dificuldade == 2 else float('inf')
        l, c = melhor_jogada(game, debug_mode, jogador, alturamax)
        game[l][c] = jogador

def jogar():
    game =  [[' ',' ',' '],
             [' ',' ',' '],
             [' ',' ',' ']]
    
    print(" ------ Jogo da Velha com IA Minimax com Poda Alpha-Beta ----- ")
    print("Modo de jogo: ")
    print("1 - Humano x Humano")
    print("2 - Humano x IA")
    modo_jogo = int(input())

    if modo_jogo == 2:
        print("Primeiro jogador: ")
        print("1 - Humano começa")
        print("2 - IA começa")
        primeiro = int(input())

        print("Dificuldade")
        print("1 - Fácil")
        print("2 - Médio")
        print("3 - Difícil")
        dificuldade = int(input())

        print(" Modo debug: ")
        print("1 - Mostrar todos os nós")
        print("2 - Mostrar apenas nós folha")
        print("3 - Jogo sem debug")
        debug_mode = int(input())

    for rodada in range(9):
        imprimir_tabuleiro(game)
        jogador = 'X' if rodada % 2 == 0 else 'O'
        
        if modo_jogo == 1 or (modo_jogo == 2 and ((rodada % 2 == 0 and primeiro == 1) or (rodada % 2 == 1 and primeiro == 2))):
            while True:
                posicao = int(input(f"{jogador}, escolha uma posição (1-9): "))
                if posicao_valida(game, posicao):
                    break
                else:
                    print("Posição inválida. Tente novamente.")
            l, c = pos(posicao)
            game[l][c] = jogador
        else:
            print("A IA está pensando...")
            if rodada != 0:
                jogada_ia(game, debug_mode, jogador, dificuldade)
            else:
                l,c = pos(random.randint(1, 9))
                game[l][c] = jogador
                

        if checar_vitoria(game):
            imprimir_tabuleiro(game)
            print(f"{jogador} ganhou!")
            return

    imprimir_tabuleiro(game)
    print("Deu velha!")

# Iniciar o jogo
jogar()
