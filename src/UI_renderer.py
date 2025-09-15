import tkinter as tk
from tkinter import messagebox
from cell import Cell
from gameLogic import GameLogic

class GameGUI:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.mineCount = None
        self.statusLabel = None
        self.game = GameLogic
    
    def renderBoard(self):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=3, command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def run(self):
        self.root.mainloop()

    def renderCell(self, cell:Cell, row:int, col:int):
        pass

    def updateStatus(self, status:str):
        pass

    def updateMineCount(self, count:int):
        pass