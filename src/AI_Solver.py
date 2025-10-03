"""
File: AI_Solver.py
Module: AISolver
Description:
    This AI Solver competes with the Player using one of three difficulties: easy, medium, or hard. 
    The solver takes turns with the user revealing a cell on the board, and the first to hit a mine loses.
    Easy randomly clicks any cell on the board, while the medium and hard implement increasingly complex reasoning.

Inputs:
    - difficulty (string) -- either "Easy", "Medium", or "Hard"
Outputs:
    - None -- it interacts with the board by revealing cells
    
Authors: Connor Anderson

Creation Date: 10/01/2025
"""
# imports all necessary classes and APIs
from tkinter import messagebox
from board_manager import BoardManager
import random

# creates GUI class object
class AISolver:
    def __init__(self, difficulty, board_mgr):
        # the difficulty it was initialized with ("Easy", "Medium", or "Hard")
        self.difficulty = difficulty

        # this will hold the function to be ran by the solver (different for each difficulty)
        self.reveal = None 

        self.board_mgr = board_mgr
        
        # set the 
        match difficulty:
            case "Easy":
                self.reveal = self.easy
            case "Medium":
                self.reveal = self.medium
            case "Hard":
                self.reveal = self.hard
            case "_":
                raise TypeError("Invalid Difficulty for AI Solver")
                
                

    # this is for the AI to take its turn
    def play_turn(self, reveal, setFlag):
        # this will call the respective function (easy, medium, or hard) determined during initialization
        self.reveal(reveal,setFlag) 


    # the easy function
    def easy(self,reveal, setFLag):
        # messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.easy()")
        untouched = self.board_mgr.untouched_cells()
        cell_to_uncover = random.choice(untouched)
        #we have to set the flag state to false so that it doesn't place flags when flag_mode is on
        flag_state = setFLag(False)
        reveal(cell_to_uncover[0],cell_to_uncover[1])
        setFLag(flag_state)

    # the medium function
    def medium(self,reveal,setFlag):
        #Iterate through the whole grid of cells
        # messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.medium()")
        size = len(self.board_mgr.grid)
        for row in range(size):
            for col in range(size):
                cell = self.board_mgr.get_cell(row,col)
                if cell.is_revealed:
                    hidden = []
                    flagged = 0
                    #The next 5 lines get all the hidden and flagged cells
                    neighboors = self.board_mgr.neighbors(row,col) #Gets list of neighboor coordinates
                    for nrow,ncol in neighboors:
                        #Iterates through the coordinates of each of the 8 neighboors
                        neighboor = self.board_mgr.get_cell(nrow,ncol) 
                        if not neighboor.is_revealed: hidden.append((nrow,ncol)) #checks if cell has been revealed
                        if neighboor.has_flag: flagged += 1 #checks if cell is flagged
                    if len(hidden) == cell.neighbor_count:
                        #If the cell number is the same as the number of adjacent hidden tiles, flag all adjacent hidden tiles
                        for hrow,hcol in hidden:
                            if (not self.board_mgr.is_flagged(hrow,hcol)):
                                flag_state = setFlag(True) 
                                reveal(hrow,hcol)
                                setFlag(flag_state)
                    if flagged == cell.neighbor_count:
                        #If the number of adjacent flagged cells is the same as the cell number, reveal all remaining adjecent non flagged cells
                        for hrow,hcol in hidden: 
                            if self.board_mgr.is_flagged(hrow,hcol):
                                continue
                            #we have to set the flag state to false so that it doesn't place flags when flag_mode is on
                            flag_state = setFlag(False)
                            reveal(hrow,hcol)
                            setFlag(flag_state)
                            return
        # If none of the first two rules apply, choose a random cell 
        self.easy(reveal, setFlag)

    # the hard function
    def hard(self):
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.hard()")

    # We could define get() and set() functions here for the AI Solver's difficulty if it could be changed, but currently the game does not restart