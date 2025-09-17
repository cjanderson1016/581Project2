import tkinter as tk
from tkinter import messagebox


class GameGUI:
    def __init__(self, game_logic):
        self.game = game_logic
        self.board = game_logic.board_mgr.grid
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.buttons = [[None for _ in range(len(self.board))] for _ in range(len(self.board))]
        self.mine_count = None
        self.status_label = None
    
    def renderBoard(self):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=6, height=3, font=('Arial', 24), command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def run(self):
        self.renderBoard()
        self.root.mainloop()

    def renderCell(self, row:int, col:int, flag:bool):
        cell = self.board[row][col]
        if flag:
            self.buttons[row][col].config(text='F', font=('Arial', 24))
        elif cell.has_mine:
            self.updateStatus("Game Over")
            messagebox.showinfo("Game Over", "You have hit a mine!")
            self.buttons[row][col].config(text='*', bg='red', font=('Arial', 24))
        else:
            # Show the neighbor count including zero
            self.buttons[row][col].config(text=str(cell.neighbor_count), bg='lightgray', font=('Arial', 24))

    def updateStatus(self, status:str):
        pass

    def updateMineCount(self, count:int):
        self.mineCount = int

    def reveal(self, row: int, col: int):
        revealed_cells = self.game.reveal_cell(row, col)
        for r, c in revealed_cells:
            self.renderCell(r, c, False)

    def endGame(self):
        pass
