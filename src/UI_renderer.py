import tkinter as tk
from tkinter import messagebox
from board_manager import BoardManager
from game_logic import GameLogic


class GameGUI:
    def __init__(self):
        # Initializes all necessary variables for GUI management to make updates to the user interface
        self.game = None
        self.board = None
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.buttons = None
        self.mine_count = None
        self.status_label = None
        self.user_mine_count = tk.StringVar()
        self.label = None
        self.mine_entry = None
        self.start_button = None
        self.board_manager = None
        self.flag_mode = False
        # calls the get mine count upon initialization to prompt user for mine count
        self.getMineCount()
    # renders board as grid of buttons based on length 10
    def renderBoard(self):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=4, height=2, font=('Arial', 10), command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button
    # loops GUI to maintain display 
    def run(self):
        self.root.mainloop()
    # adds graphic to cell depending on status
    def renderCell(self, row:int, col:int, flag:bool):
        cell = self.board[row][col]
        if flag:
            self.buttons[row][col].config(text='🚩',bg="yellow", font=('Arial', 10))
        elif cell.has_mine:
            self.updateStatus("Game Over")
            messagebox.showinfo("Game Over", "You have hit a mine!")
            self.buttons[row][col].config(text='*', bg='red', font=('Arial', 10))
        elif cell.is_revealed:
            # Show the neighbor count including zero
            self.buttons[row][col].config(text=str(cell.neighbor_count), bg='lightgray', font=('Arial', 10))
        else:
            self.buttons[row][col].config(text=' ', bg='SystemButtonFace',font=('Arial',10))
    # creates initial frame for user input of mines
    def getMineCount(self):
        self.label = tk.Label(self.root, text = "Enter mine count: ")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.mine_entry = tk.Entry(self.root, textvariable=self.user_mine_count)
        self.mine_entry.grid(row=0,column=1, padx=10,pady=10)
        self.start_button = tk.Button(self.root, text="Start Game", command=self.startGame)
        self.start_button.grid(row=1, column=0, columnspan=2, rowspan=2, pady=10)
    # reveals selected cell or adds flag if in flag mode, also handles win/loss functionality
    def reveal(self, row: int, col: int):
        if self.flag_mode:
            self.addFlag(row, col)
            return
        revealed_cells = self.game.reveal_cell(row, col)
        for r, c in revealed_cells:
            self.renderCell(r, c, False)
        
        if self.game.revealed_safe_cells == self.game.total_safe_cells:
            messagebox.showinfo("Victory!", "You revealed all safe cells. You win!")
            self.updateStatus("Winner")
    # validates input to mine count and begins building board and initializing game
    def startGame(self):
        try:
            self.mine_count = int(self.user_mine_count.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Mine Count must be entered as a number.")
            return
        if self.mine_count < 0 or self.mine_count > 51:
            messagebox.showwarning("Invalid number of mines!", "Please enter a number between 1 and 50")
            return

        self.board_manager = BoardManager(grid_size=10, mine_count=self.mine_count)
        self.game = GameLogic(board_mgr=self.board_manager)
        self.board = self.board_manager.grid
        self.buttons = [[None for _ in range(len(self.board))] for _ in range(len(self.board))]
        self.label.destroy()
        self.mine_entry.destroy()
        self.start_button.destroy()
        self.renderBoard()
        flag_toggle = tk.Button(self.root, text="Toggle Flag Mode", command=self.toggleFlag)
        flag_toggle.grid(row=len(self.board), column=0,columnspan=len(self.board),pady=10)
    # toggle flag mode and update status
    def toggleFlag(self):
        self.flag_mode = not self.flag_mode
        mode = "Flag" if self.flag_mode else "Reveal"
        self.updateStatus(f"Mode: {mode}")
    # adds flags to cells, and prints warning if out of flags
    def addFlag(self, row, col):
        result = self.game.toggle_flag(row,col)
        if result == 0:
            messagebox.showwarning("Out of flags","You are out of Flags")
            return
        else:
            self.renderCell(row, col, self.game.board_mgr.get_cell(row=row,column=col).has_flag)
    # updates status label at bottom of screen
    def updateStatus(self, status:str):
        if self.status_label is None:
            self.status_label = tk.Label(self.root, text=status)
            self.status_label.grid(row=len(self.board)+1,column=0, columnspan=len(self.board), pady=5)
        else:
            self.status_label.config(text=status)
