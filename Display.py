import tkinter as tk

class Display:
    def __init__(self):
        self.root = tk.Tk()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = tk.Label(self.root, text="Sua vez!", font=('Arial', 24, 'bold'))

        self.root.title("Jogo da Velha")

    def initbuttons(self, on_click):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', width=13, height=5, 
                                                bg="#BC00C0", activebackground="#c0c0c0",
                                                font=('Helvetica', 24, 'bold'), 
                                                command=lambda i=i, j=j: on_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)


    def update_buttons(self,game):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=game[i][j])
    
    def endgame(self, jogador):
        if jogador:
            self.status_label.config(text=f"Jogador {jogador} venceu!")
        else:
            self.status_label.config(text="Deu Velha!")