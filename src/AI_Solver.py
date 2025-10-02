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

# creates GUI class object
class AISolver:
    def __init__(self, difficulty):
        # the difficulty it was initialized with ("Easy", "Medium", or "Hard")
        self.difficulty = difficulty

        # this will hold the function to be ran by the solver (different for each difficulty)
        self.reveal = None 
        
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
    def play_turn(self):
        # this will call the respective function (easy, medium, or hard) determined during initialization
        self.reveal() 


    # the easy function
    def easy(self):
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.easy()")

    # the medium function
    def medium(self):
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.medium()")

    # the hard function
    def hard(self):
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.hard()")

    # We could define get() and set() functions here for the AI Solver's difficulty if it could be changed, but currently the game does not restart