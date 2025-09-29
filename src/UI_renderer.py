"""
File: UI_renderer.py
Module: GameGUI
Description:
    This GUI uses tkinter to create a grid of buttons that can be clicked on by the player to reveal either a safe cell with a count of neighbors having a mine, or a mine. 
    The GUI also has flagging and win loss notification functionalities.
Purpose: 
    - To display a GUI that can be interacted with by the user while maintaining the logic of the game.
Inputs:
    - User specified mine count
    - User inputs in the form of button clicking. 
    - Cell coordinates 
    - Boolean variables
Outputs:
    - Updates screen according to game logic and inputs from the user
    - Update the mine count
    - Produces warning messages as needed when out of bounds
    
Authors: Genea Dinnall, Sam Kelemen, Meg Taggart

Creation Date: 09/17/2025
"""
# imports all necessary classes and APIs
import time
import tkinter as tk
from tkinter import messagebox
from board_manager import BoardManager
from game_logic import GameLogic

# creates GUI class object
class GameGUI:
    def __init__(self):
        # Initializes all necessary variables for GUI management to make updates to the user interface
        # Initializes 
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
        self.AI_label = None
        self.AI_difficulty = None
        self.start_button = None
        self.board_manager = None
        self.flag_mode = False
        self.start_time = None
        self.timer_label = tk.Label(self.root, text="Time: 0")
        self.running = False
        # calls the get mine count upon initialization to prompt user for mine count
        self.getMineCount()
        self.getAIDifficulty()

    # renders board as grid of buttons based on length 10
    def renderBoard(self):
        # show timer
        self.timer_label.grid(row=0, column=0,columnspan=10, pady=5, sticky="n") # stretch it across all 10 columns, center it, and pad it

        for y in range(len(self.board)):
            for x in range(len(self.board)):
                button = tk.Button(self.root, text=' ', width=4, height=2, font=('Arial', 10), command=lambda y=y, x=x: self.reveal(y,x))
                button.grid(row=(y+1), column=(x+1))
                self.buttons[y][x] = button

    # loops GUI to maintain display 
    def run(self):
        self.root.mainloop()
    # adds graphic to cell depending on status
    def renderCell(self, row:int, col:int, flag:bool):
        cell = self.board[row][col]
        # handles if cell is a flag cell
        if flag:
            self.buttons[row][col].config(text='🚩',bg="yellow", font=('Arial', 10))
        # mine cell handling
        elif cell.has_mine:
            
            # stop the timer
            self.stop_timer()

            # indicate loss
            self.updateStatus("Game Over")
            messagebox.showinfo("Game Over", "You have hit a mine!")
            self.buttons[row][col].config(text='*', bg='red', font=('Arial', 10))
        # revealed neighbor handling
        elif cell.is_revealed:
            # Show the neighbor count including zero
            self.buttons[row][col].config(text=str(cell.neighbor_count), bg='lightgray', font=('Arial', 10))
        # return to covered state if already a flag while in flag mode
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
    # gets the difficulty of the AI
    def getAIDifficulty(self):
        options = ["Easy", "Medium", "Hard"]
        
        self.AI_label = tk.Label(self.root, text = "Choose Difficulty")
        self.AI_difficulty = tk.
    # reveals selected cell or adds flag if in flag mode, also handles win/loss functionality
    def reveal(self, row: int, col: int):
        if self.flag_mode:
            self.addFlag(row, col)
            return
        
        # if it is the first click (reveal), start the timer
        if self.game.is_first_click:
            self.start_timer()

        # reveal the cell in GameLogic (if it is the first click, this will set is_first_click to False)
        revealed_cells = self.game.reveal_cell(row, col)
        for r, c in revealed_cells:
            self.renderCell(r, c, False)
        
        if self.game.revealed_safe_cells == self.game.total_safe_cells:
            # stop timer
            self.stop_timer()

            # indicate victory
            messagebox.showinfo("Victory!", "You revealed all safe cells. You win!")
            self.updateStatus("Winner")
    # validates input to mine count and begins building board and initializing game
    def startGame(self):
        try:
            self.mine_count = int(self.user_mine_count.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Mine Count must be entered as a number.")
            return
        if self.mine_count < 10 or self.mine_count > 20:
            messagebox.showwarning("Invalid number of mines!", "Please enter a number between 10 and 20")
            return

        self.board_manager = BoardManager(grid_size=10, mine_count=self.mine_count)
        self.game = GameLogic(board_mgr=self.board_manager)
        self.board = self.board_manager.grid
        self.buttons = [[None for _ in range(len(self.board))] for _ in range(len(self.board))]
        # destroys unnecessary components to render board
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

    # starts the timer
    def start_timer(self):
        self.start_time = time.time() # record the start time
        self.running = True # set running to True to indicate the timer is running
        self.update_timer() # call the update_timer function

    # stops the timer by setting the global 'running' to False (read in update_timer)
    def stop_timer(self):
        self.running = False

    # calls itself to update the timer every second until self.running is set to False
    def update_timer(self):
        # if the timer is running, update the timer, then call itself after 1 second has passed
        if self.running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}")
            # call this method again after 1000 ms (1 sec)
            self.root.after(1000, self.update_timer)