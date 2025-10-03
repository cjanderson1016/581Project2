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
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.easy()")
        untouched = self.board_mgr.untouched_cells()
        cell_to_uncover = random.choice(untouched)
        #we have to set the flag state to false so that it doesn't place flags when flag_mode is on
        flag_state = setFLag(False)
        reveal(cell_to_uncover[0],cell_to_uncover[1])
        setFLag(flag_state)

    # the medium function
    def medium(self,reveal,setFlag):
        #Iterate through the whole grid of cells
        messagebox.showinfo(message=f"AI Solver (difficulty: {self.difficulty}) called self.medium()")
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
    
Authors: Connor Anderson, Mohamed Ashraq

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
    def hard(self, reveal, setFlag):
        size = len(self.board_mgr.grid)

        # Medium rules
        for row in range(size):
            for col in range(size):
                cell = self.board_mgr.get_cell(row, col)
                if not cell.is_revealed:
                    continue

                hidden = []
                flagged = 0
                #The next lines get all the hidden and flagged cells
                neighbors = self.board_mgr.neighbors(row, col)  # Gets list of neighbor coordinates
                for nrow, ncol in neighbors:
                    #Iterates through the coordinates of each of the 8 neighbors
                    ncell = self.board_mgr.get_cell(nrow, ncol)
                    if not ncell.is_revealed:
                        hidden.append((nrow, ncol))  # checks if cell has been revealed
                    if ncell.has_flag:
                        flagged += 1                # checks if cell is flagged

                # Rule 1: if #hidden == number -> all hidden are mines
                if hidden and len(hidden) == cell.neighbor_count:
                    for hr, hc in hidden:
                        if not self.board_mgr.is_flagged(hr, hc):
                            # we have to set the flag state to true so that it places a flag
                            prev = setFlag(True)
                            reveal(hr, hc)
                            setFlag(prev)
                            return

                # Rule 2: if #flagged == number -> remaining hidden are safe 
                if hidden and flagged == cell.neighbor_count:
                    for hr, hc in hidden:
                        if not self.board_mgr.is_flagged(hr, hc):
                            # we have to set the flag state to false so that it doesn't place flags when flag_mode is on
                            prev = setFlag(False)
                            reveal(hr, hc)
                            setFlag(prev)
                            return

        # 1-2-1 pattern from horizontal & vertical 
        if self._apply_121_patterns(reveal, setFlag):
            return

        # If none of the rules apply choose a random cell easy mode
        self.easy(reveal, setFlag)


    #Helpers
    def _in_bounds(self, r, c) -> bool:
        n = self.board_mgr.grid_size
        return 0 <= r < n and 0 <= c < n

    def _apply_121_patterns(self, reveal, setFlag) -> bool:
        size = len(self.board_mgr.grid)

        # Horizontal 1-2-1
        for r in range(size):
            for c in range(1, size - 1):
                left  = self.board_mgr.get_cell(r, c - 1)
                mid   = self.board_mgr.get_cell(r, c)
                right = self.board_mgr.get_cell(r, c + 1)
                if not (left.is_revealed and mid.is_revealed and right.is_revealed):
                    continue
                if not (left.neighbor_count == 1 and mid.neighbor_count == 2 and right.neighbor_count == 1):
                    continue

                # Check the hidden strip directly above or below the 1-2-1 trio
                for dr in (-1, 1):
                    rr = r + dr
                    if not self._in_bounds(rr, c):
                        continue
                    a = (rr, c - 1)  # outer (mine)
                    b = (rr, c)      # inner (safe)
                    d = (rr, c + 1)  # outer (mine)

                    # Must be in-bounds and currently hidden
                    if not (self._in_bounds(*a) and self._in_bounds(*b) and self._in_bounds(*d)):
                        continue
                    if self.board_mgr.get_cell(*a).is_revealed: 
                        continue
                    if self.board_mgr.get_cell(*b).is_revealed: 
                        continue
                    if self.board_mgr.get_cell(*d).is_revealed: 
                        continue

                    # Reveal the middle safe tile, then return
                    prev = setFlag(False)
                    reveal(*b)
                    setFlag(prev)
                    return True

        # Vertical 1-2-1
        for r in range(1, size - 1):
            for c in range(size):
                top = self.board_mgr.get_cell(r - 1, c)
                mid = self.board_mgr.get_cell(r, c)
                bot = self.board_mgr.get_cell(r + 1, c)
                if not (top.is_revealed and mid.is_revealed and bot.is_revealed):
                    continue
                if not (top.neighbor_count == 1 and mid.neighbor_count == 2 and bot.neighbor_count == 1):
                    continue

                # Check the hidden strip directly left or right of the 1-2-1 
                for dc in (-1, 1):
                    cc = c + dc
                    if not self._in_bounds(r, cc):
                        continue
                    a = (r - 1, cc)  # outer (mine)
                    b = (r, cc)      # inner (safe)
                    d = (r + 1, cc)  # outer (mine)

                    if not (self._in_bounds(*a) and self._in_bounds(*b) and self._in_bounds(*d)):
                        continue
                    if self.board_mgr.get_cell(*a).is_revealed: 
                        continue
                    if self.board_mgr.get_cell(*b).is_revealed: 
                        continue
                    if self.board_mgr.get_cell(*d).is_revealed: 
                        continue

                    
                    prev = setFlag(False)
                    reveal(*b)
                    setFlag(prev)
                    return True

        # No 1-2-1 action found
        return False

