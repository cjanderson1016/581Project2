"""
File: game_logic.py
Module: GameLogic
Purpose:
    Implements core Minesweeper gameplay independent of UI: flag toggling, safe first-click mine placement, 
    revealing cells, and win/loss detection.

Inputs:
    - A BoardManager instance supplied at construction. The UI
      calls GameLogic methods in response to user actions.

Outputs:
    - toggle_flag(...) -> int: row, col for flags placed/removed.
    - reveal_cell(...) -> List[Tuple[int,int]]: coordinates newly revealed cells.
    - Game state mutations on the underlying BoardManager grid (cell flags,
      cell revealed states, mine placement) and GameLogic state (counters, flags).

Author: Jenny Tsotezo, Matthew Eagleman

Created: 2025-09-17
"""

from typing import List, Tuple
from board_manager import BoardManager
import random

class GameLogic:
    # Construct a GameLogic bound to a specific BoardManager.
    # Parameters: board_mgr (BoardManager): The board service that stores cells and performs mine placement / neighboring computations.
    # Returns: None
    # Initializes gameplay state and computes initial total_safe_cells from the current board_mgr.mine_count.
    def __init__(self, board_mgr: BoardManager):
        self.board_mgr = board_mgr
        # Delay mine placement until first reveal to guarantee safety.
        self.is_first_click: bool = True
        # Blocks further actions when True (loss or win).
        self.is_game_over: bool = False
         # keeps track of the count of revealed safe cells
        self.revealed_safe_cells: int = 0
         # Keeps track of the total safe cells from the very beginning of the game.
        # It is calculated by subtracting the number of mines from the total number of cells.
        self.total_safe_cells: int = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count
         # Tracks how many flags the user has placed
        self.flags_placed: int = 0
        # Stores the difficulty of the AI
        self.AI_diff = None

    # Start a brand-new round with a specified mine count. Clears prior state and prepares for a safe first click (mines not yet placed).
    # Parameters: mine_count (int): Number of mines for the new game (e.g., 10–20).
    # Returns: None
    # Calls BoardManager.reset(mine_count) to rebuild an empty grid.
    # Resets is_first_click, is_game_over, revealed_safe_cells, flags_placed, and recomputes total_safe_cells.
    # Reset all state for a new game with a given mine count
    def reset_game(self, mine_count: int):
         # Recreate an empty grid with new mine count.
        self.board_mgr.reset(mine_count)
        # Next reveal will be treated as the first click.
        self.is_first_click = True
        # Re-initialize all variables to zero inorder to restart the game
        self.is_game_over = False
        # Reset the number of revealved safe cells to zero inorder to start a new game
        self.revealed_safe_cells = 0
        # Number of flags reset to zero.
        self.flags_placed = 0
        # Recompute safe cells in case mine_count changed
        self.total_safe_cells = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count
        self.did_win: bool = False

    # Place or remove a flag on a covered cell, enforcing the rule that you cannot place more flags than the total number of mines.
    # Parameters: row (int): Row index of the target cell.
    #           - col (int): Column index of the target cell.
    # Returns: int: +1  if a flag was successfully placed,
    #               -1  if an existing flag was removed,
    #                0  if no change (e.g., game over, cell already revealed, or flag limit would be exceeded).
    def toggle_flag(self, row: int, col: int) -> int:
        # Do not allow flagging after the game ended.
        if self.is_game_over:
            return 0
        # Locate the target cell on the board.
        cell = self.board_mgr.get_cell(row, col)
        # You cannot flag an already-revealed cell.
        if cell.is_revealed:
            return 0
        # You cannot place more flags than total mines.
        if not cell.has_flag and self.flags_placed >= self.board_mgr.mine_count:
            return 0
        cell.has_flag = not cell.has_flag
        # Keep the running count in sync.
        self.flags_placed += 1 if cell.has_flag else -1
        # If the number of flags you've placed equals the total number of mines
        # AND every mine location actually has a flag on it
        if self.flags_placed == self.board_mgr.mine_count and self._all_mines_flagged():
            self.is_game_over = True   # end the game…
            self.did_win = True        # and mark it as a victory.
        return 1 if cell.has_flag else -1
    
    # Reveal a cell. On the very first reveal, place mines *after* the click to guarantee safety at (row, col). If the cell is a mine, set loss. 
    # If the cell is safe: Reveal it, and if its neighbor_count is zero, flood-reveal adjacent cells (including diagonals).
    #                    - Track victory when all non-mine cells are revealed.
    # Parameters: row (int): Row index of the cell to reveal.
    #           - col (int): Column index of the cell to reveal.
    # Returns: List[Tuple[int,int]]: Coordinates of all cells newly revealed during this action. If a mine is revealed, returns
    # a single coordinate [(row, col)] to allow the UI to mark the hit.
    # On first-click, calls BoardManager.place_mines(row, col) and recomputes total_safe_cells.
    def reveal_cell(self, row: int, col: int) -> List[Tuple[int, int]]:
        # Ignore reveals after win/loss.
        if self.is_game_over:
            return []
        # Get the cell to reveal.
        cell = self.board_mgr.get_cell(row, col)
        # Don’t reveal cell if it is already open or if the user flagged it.
        if cell.is_revealed or cell.has_flag:
            return []

        # First reveal of the game. make the board safe for this click.
        if self.is_first_click:
            # Place mines now, excluding the first-click (and maybe neighbors).
            self.board_mgr.place_mines(row, col)
            # Recompute safe target in case mine_count differs.
            self.total_safe_cells = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count
            # Make subsequent reveals are normal.
            self.is_first_click = False

        # If we hit a mine 
        if cell.has_mine:
            # The game ends
            self.is_game_over = True
            # Player loses the game
            self.did_win = False
            #return the detonated coordinate for the UI to render.
            return [(row, col)]

        # Collect every cell that becomes visible from this action.
        newly_revealed = []
        # Reveal clicked cell; if it’s a 0, cascade to neighbors.
        self._flood_reveal(row, col, newly_revealed)

        # All safe cells are revealed, player wins the game
        if self.revealed_safe_cells >= self.total_safe_cells and not self.is_game_over:
            self.is_game_over = True
            self.did_win = True
        return newly_revealed
    
    # Return True only if the flag layout exactly matches the mine layout:
    #  - every mined cell is flagged, AND
    # - no non-mined cell is flagged.
    def _all_mines_flagged(self) -> bool:
        n = self.board_mgr.grid_size 
        # Iterate over all row indices 0..n-1          
        for r in range(n): 
            # Iterate over all column indices 0..n-1                     
            for c in range(n):                  
                # Access the Cell at (r, c)
                cell = self.board_mgr.get_cell(r, c)   
                # If the cell's mine status and flag status differ, the configuration is not "perfect":
                # mined but not flagged  OR safe but flagged
                if cell.has_mine != cell.has_flag:
                    # Early exit: as soon as one mismatch is found, it's not a perfect match
                    return False                
        # If we scanned every cell without mismatch, all mines are flagged AND no safe cell is flagged
        return True                             

    
    # Perform the classic Minesweeper "cascade" from a starting cell: reveal the starting safe cell; if its neighbor_count == 0, expand
    # to all 8-directional neighbors, continuing until the zero region and its numbered boundaries are exposed.
    # Parameters: row (int): Starting row index.
    #           - col (int): Starting column index.
    # Returns: None 
    # Uses an explicit stack for iterative DFS.
    # Maintains a visited set to avoid reprocessing the same coordinates.
    # Skips mines, flagged cells, and already revealed cells.
    # When a zero is revealed, pushes its neighbors on the stack.
    def _flood_reveal(self, row: int, col: int, out_list: List[Tuple[int, int]]):
        # Use an explicit stack for iterative depth first search (no recursion limits)
        stack = [(row, col)]
        # Tracks which coordinates have processed to avoid repeats.
        visited = set()
    
        # Process until there are no more cells to visit.
        while stack:
            r, c = stack.pop()
            # Skip cell has already been handled.
            if (r, c) in visited:
                continue
            # Mark as handled so we don’t process it again.
            visited.add((r, c))
    
            # Access the actual cell object.
            cell = self.board_mgr.get_cell(r, c)
            # Never automatically open revealed cells, flags, or mines.
            if cell.is_revealed or cell.has_flag or cell.has_mine:
                continue
            
            # Reveal this safe covered cell.
            cell.is_revealed = True
            # Increment global count used for win detection.
            self.revealed_safe_cells += 1
            out_list.append((r, c))

            # Only expand when the number shown is zero.
            if cell.neighbor_count == 0:
                # Visit all 8 neighbors of the current cell
                for nr, nc in self.board_mgr.neighbors(r, c):
                    # Peek at the neighbor cell.
                    ncell = self.board_mgr.get_cell(nr, nc)
                     # Peek at the neighboring cell.
                    if not ncell.is_revealed and not ncell.has_flag and not ncell.has_mine:
                        # Schedule neighboring cell to be processed
                        stack.append((nr, nc))
    
    #Easy: The computer clicks on any hidden cell at random.
    def easy(self,reveal, setFLag):
        untouched = self.board_mgr.untouched_cells()
        cell_to_uncover = random.choice(untouched)
        #we have to set the flag state to false so that it doesn't place flags when flag_mode is on
        flag_state = setFLag(False)
        reveal(cell_to_uncover[0],cell_to_uncover[1])
        setFLag(flag_state)

    ''' 
    Medium: The computer applies two basic rules. 
    - First, if the number of hidden neighbors of a revealed cell equals that cell’s number, the AI should 
      flag all hidden neighbors. 
    - Second, if the number of flagged neighbors of a revealed cell equals that cell’s number, the AI 
      should open all other hidden neighbors. 
    - If no rule applies, the AI should pick a random hidden cell.
    '''
    def medium(self,reveal,setFlag):
        #Iterate through the whole grid of cells
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