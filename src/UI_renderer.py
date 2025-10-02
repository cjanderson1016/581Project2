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
    
Authors: Genea Dinnall, Sam Kelemen, Meg Taggart, Matthew Eagleman

Creation Date: 09/17/2025
"""
# imports all necessary classes and APIs
import time
import tkinter as tk
from tkinter import messagebox
from board_manager import BoardManager
from game_logic import GameLogic
from AI_Solver import AISolver

# creates GUI class object
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
        self.AI_label = None
        self.AI_difficulty = None
        self.AI_diff_choice = tk.StringVar()
        self.start_button = None
        self.board_manager = None
        self.flag_mode = False
        self.start_time = None
        self.timer_label = tk.Label(self.root, text="Time: 0")
        self.running = False
        
        self.turn = 1 # the turn counter (to be incremented after each move made by the AI Solver)
        self.turn_label = tk.Label(self.root, text="Turn: 1") # the initial turn label
        self.ai = None # to be initialized in startGame if the player chooses to play againt the AI (after the AI difficulty was selected)
        self.ai_diff = None # to hold the string corelating to the ai difficulty
        self.ai_active = False # indicate if there is an active AI Solver

        # calls the get mine count upon initialization to prompt user for mine count
        self.getMineCount()
        self.getAIDifficulty()

    # renders board as grid of buttons based on length 10
    def renderBoard(self):
        if (self.ai_active): # if playing against the ai, show both the timer and turns
            # show timer
            self.timer_label.grid(row=0, column=2,columnspan=5, pady=5, sticky="n") # stretch it across first 5 columns, center it, and pad it
            # show turns
            self.turn_label.grid(row=0, column=5,columnspan=5, pady=5, sticky="n") # stretch it across second 5 columns, center it, and pad it
        else: # if no ai, only show the timer
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
        self.start_button.grid(row=2, column=0, columnspan=2, rowspan=2, pady=10)

    # creates a dropdown menu for the player to choose the difficulty of the AI
    def getAIDifficulty(self):
        self.AI_diff_choice.set("Easy")
        self.AI_label = tk.Label(self.root, text = "Choose AI Difficulty:")
        self.AI_difficulty = tk.OptionMenu(self.root, self.AI_diff_choice, "None", "Easy", "Medium", "Hard")
        self.AI_label.grid(row=1, column=0, padx=10)
        self.AI_difficulty.grid(row=1, column=1, padx=10)

    # reveals selected cell or adds flag if in flag mode, also handles win/loss functionality
    def reveal(self, row: int, col: int):
        if self.flag_mode:
            self.addFlag(row, col)
            return
        
        # if it is the first click (reveal), start the timer
        if self.game.is_first_click:
            self.start_timer()

        # reveal the cell in GameLogic (if it is the first click, this will set is_first_click to False)
        revealed_cells = self.game.reveal_cell(row, col) # returns a list of the cells that were revealed by this call (empty list if nothing was revealed -- ex. clicking on a flagged cell)
        for r, c in revealed_cells:
            self.renderCell(r, c, False)
        
        # check if the board was completed -- game over
        if self.game.revealed_safe_cells == self.game.total_safe_cells:
            # stop timer
            self.stop_timer()

            if(self.ai_active): # the player completed the board against the ai -- Draw
                # indicate draw
                messagebox.showinfo("Draw...", "No one blew up!")
                self.updateStatus("Draw")
            else: # if it was single player -- Victory!
                # indicate victory
                messagebox.showinfo("Victory!", "You revealed all safe cells. You win!")
                self.updateStatus("Winner")
        
        # if...
        #   1. the game is not over
        #   2. the ai solver is on
        #   3. cells were revealed (i.e. the player did not just click on a flagged cell)
        # then control is passed to the ai solver...
        if (not self.game.is_game_over) and (self.ai_active) and (revealed_cells): 
            self.ai.play_turn() # the ai makes its decision
            # === after the ai makes its turn === #
            if(not self.game.is_game_over): # the ai did not lose and the game continues  
                self.turn += 1 # increment the turn counter now that both the player and AI have done their turns
                self.update_turn(self.turn) # update the label with the new turn count
            elif self.game.revealed_safe_cells == self.game.total_safe_cells: # the ai completed the board
                # indicate draw
                messagebox.showinfo("Draw...", "No one blew up!")
                self.updateStatus("Draw")
            else: # the game is over meaining the ai clicked a bomb
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
        
        self.ai_diff = self.AI_diff_choice.get() # retrieve the ai difficulty value (string) from the dropdown
        self.game.AI_diff = self.ai_diff # share the string to the GameLogic
        # if the player wants to play against the ai (i.e. they did not select "None"), initialize the AI Solver and set ai_active to True
        if self.ai_diff != "None":
            self.ai_active = True
            self.ai = AISolver(self.ai_diff)

        self.board = self.board_manager.grid
        self.buttons = [[None for _ in range(len(self.board))] for _ in range(len(self.board))]
        # destroys unnecessary components to render board
        self.label.destroy()
        self.mine_entry.destroy()
        self.start_button.destroy()
        self.renderBoard()
        flag_toggle = tk.Button(self.root, text="Toggle Flag Mode", command=self.toggleFlag)
        flag_toggle.grid(row=len(self.board)+1, column=0,columnspan=len(self.board),pady=10) # Added +1 to the row so its not overlapping with the board
        # Button for testing easy AI difficulty
        # easy = tk.Button(self.root, text="Easy AI Test", command=self.easy)
        # easy.grid(row=len(self.board)+2,column=0, columnspan=3)
        # # Button for testing medium AI difficulty
        # medium = tk.Button(self.root, text="Medium AI Test", command=self.medium)
        # medium.grid(row=len(self.board)+2,column=3, columnspan=3)
        # Destroy AI difficulty menu
        self.AI_label.destroy()
        self.AI_difficulty.destroy()

    #This function makes it so that the AI can use the reveal function. Its only used in the button
    def easy(self):
        self.game.easy(self.reveal, self.setFlag)

    #Same as the easy function but for medium
    def medium(self):
        self.game.medium(self.reveal,self.setFlag)

    # sets flag mode to be the given value
    def setFlag(self, value): # This function is mainly for the AI to be able to place flags
        cur_flag_state = self.flag_mode
        self.flag_mode = value
        return cur_flag_state #Return the state that the flag was in before the function
    
    # toggle flag mode and update status
    def toggleFlag(self):
        self.flag_mode = not self.flag_mode
        mode = "Flag" if self.flag_mode else "Reveal"
        self.updateStatus(f"Mode: {mode}")

    # adds flags to cells, and prints warning if out of flags
    def addFlag(self, row, col):
        result = self.game.toggle_flag(row,col)
        self.board_manager.get_cell(row,col).flag()
        if result == 0:
            messagebox.showwarning("Out of flags","You are out of Flags")
            return
        else:
            self.renderCell(row, col, self.game.board_mgr.get_cell(row=row,column=col).has_flag)

    # updates status label at bottom of screen
    def updateStatus(self, status:str):
        if self.status_label is None:
            self.status_label = tk.Label(self.root, text=status)
            self.status_label.grid(row=len(self.board)+1,column=6, columnspan=len(self.board), pady=5)
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

    # update the turn counter with the value of "turn"
    def update_turn(self, turn):
        self.turn_label.config(text=f"Turn: {turn}")