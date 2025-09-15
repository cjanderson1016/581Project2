import tkinter as tk
from tkinter import messagebox

class GameGUI:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title("Minesweeper")
    
    def buildGrid(self):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=3, command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def run(self):
        self.root.mainloop()

board = [[0,0,0],[0,0,0],[0,0,0]]
gui=GameGUI(board)
gui.run()
