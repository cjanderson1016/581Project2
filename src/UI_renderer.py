import tkinter as tk
from tkinter import messagebox


class GameGUI:
    def __init__(self, GameLogic):
        self.board = GameLogic.board
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.buttons = [[None for _ in range(len(self.board))] for _ in range(len(self.board))]
        self.mine_count = None
        self.status_label = None
        self.game = GameLogic
    
    def renderBoard(self):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=3, command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def run(self):
        self.renderBoard()
        self.root.mainloop()

    def renderCell(self, row:int, col:int, flag:bool):
        cell = self.board[row][col]
        if flag:
            self.buttons[row][col].config(text='🚩')
        if cell.has_mine and not flag:
            self.updateStatus("Game Over")
            messagebox.showinfo("You have hit a mine.")
            self.buttons[row][col].config(text='💥', bg='red')
        if cell.neighbor_count == 0 and not flag:
            pass

    def updateStatus(self, status:str):
        pass

    def updateMineCount(self, count:int):
        self.mineCount = int

    def endGame(self):
        pass
