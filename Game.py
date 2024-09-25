from Display import Display
from IA import IA

class Game:
    def __init__(self, modo_jogo: int = 2, dificuldade: int = 3, debug_mode: int = 3, primeiro:int = 1):
        self.game = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.modo_jogo = modo_jogo      # 1 para humano x humano, 2 para humano x IA
        self.dificuldade = dificuldade  # 1 - fácil, 2 - médio, 3 - difícil
        self.debug_mode = debug_mode    # 1 - mostrar todos os nós, 2 - apenas nós folha, 3 - sem debug
        self.primeiro = primeiro        # 1 para humano começar, 2 para IA começar

        self.IA = IA()
        self.display = Display()

        self.jogar()

    def jogar(self):
        self.display.initbuttons(self.on_click)
        
        self.display.status_label.grid(row=3, column=0, columnspan=3)

        # Verifica se a IA começa jogando
        if self.primeiro == 2 and self.modo_jogo == 2:
            self.display.status_label.config(text="IA está pensando...")
            self.display.root.after(200, self.IA.jogada_ia, self.game, self.debug_mode, 'X', self.dificuldade)
        
        self.display.root.mainloop()
    
    def update_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def on_click(self,i, j):
        if self.game[i][j] == ' ':
            self.game[i][j] = self.current_player
            self.display.update_buttons(self.game)
            self.update_player()    # Próxima jogada da IA

            if self.checar_vitoria():
                self.display.endgame(self.current_player)
                return
            elif all(cell != ' ' for row in self.game for cell in row):
                self.display.endgame(False)
                return
            
            if self.modo_jogo == 2:  # Humano x IA
                self.display.status_label.config(text="IA está pensando...")
                self.display.root.after(200, self.IA.jogada_ia, self.game, self.debug_mode, self.current_player, self.dificuldade, self.checar_vitoria, self.display)
                self.update_player()    # Voltando para sua jogada

    def checar_vitoria(self):
        for i in range(3):
            if self.game[i][0] == self.game[i][1] == self.game[i][2] != ' ':
                return self.game[i][0]
            if self.game[0][i] == self.game[1][i] == self.game[2][i] != ' ':
                return self.game[0][i]
        
        if self.game[0][0] == self.game[1][1] == self.game[2][2] != ' ':
            return self.game[0][0]
        if self.game[2][0] == self.game[1][1] == self.game[0][2] != ' ':
            return self.game[2][0]
        
        return False