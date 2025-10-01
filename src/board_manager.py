"""
File: board_manager.py
Module: BoardManager
Purpose:
    Define the Minesweeper board model: build a square grid of Cell objects,
    place mines after the first click with a safe zone, and maintain neighbor counts.
    UI-agnostic; used by higher-level game logic.

Inputs:
    grid_size: int (>0)
    mine_count: int (0..grid_size^2)
    place_mines(safe_row: int, safe_col: int)

Outputs:
    get_cell(row, col) -> Cell
    neighbors(row, col) -> list[tuple[int, int]]
    count_adjacent_mines(row, col) -> int
    compute_adjacent_mines() -> None
    reset(mine_count) -> None

Errors:
    ValueError for invalid sizes or unsafe mine_count
    IndexError for out-of-bounds get_cell

Author(s): Sam Kelemen, Jenny Tsotezo, Genea Dinnall, Megan Taggart
Created Date: 2025-09-17

"""

from typing import List, Tuple
from cell import Cell
import random

"""a square grid of Cell objects. Mines are
    placed after the user’s first click so that the first cell—and its 8
    neighbors are guaranteed safe, also computes per-cell neighbor mine counts."""
class BoardManager:
    """Inits an empty grid (no mines yet) of size grid_size×grid_size.
        Mine count is stored for later placement via place_mines()."""
    def __init__(self, grid_size: int, mine_count: int):
        if grid_size <= 0:
            raise ValueError("grid_size must be positive")
        if mine_count > grid_size * grid_size:
            raise ValueError("mine_count cannot exceed total number of cells")

        self.grid_size = grid_size
        self.mine_count = mine_count
        # fresh cells: no mines, neighbor_count = 0
        self.grid = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
    
    def place_mines(self, safe_row: int, safe_col: int):
        """randomly place mines while keeping the first-clicked cell and all of
        its neighbors mine-free. After placement, compute neighbor counts."""
        # all possible coordinates except the first clicked cell
        # exclude the first-click cell and all of its neighbors
        safe_zone = set(self.neighbors(safe_row, safe_col))
        safe_zone.add((safe_row, safe_col))
        # candidate cells exclude the entire safe zone
        all_coords = [
            (r, c)
            for r in range(self.grid_size)
            for c in range(self.grid_size)
            if not (r == safe_row and c == safe_col)
            if (r, c) not in safe_zone
        ]
        if self.mine_count > len(all_coords):
            raise ValueError("mine_count too large for first-click safe zone")
         # choose unique mine positions
        mine_coords = random.sample(all_coords, self.mine_count)
        
        for r, c in mine_coords:
            self.grid[r][c].has_mine = True
        # populate neighbor counts for every cell
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.grid[r][c].neighbor_count = self.count_adjacent_mines(r, c)


    def get_cell(self, row: int, column: int):
        # return the Cell at (row, column); raise if out of bounds.
        if not (0 <= row < self.grid_size and 0 <= column < self.grid_size):
            raise IndexError("cell coordinates out of range")
        return self.grid[row][column]

    def untouched_cells(self):
        # return coordinates of all unrevealed or unflagged cells
        coords = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.get_cell(row,col)
                if not cell.has_flag and not cell.is_revealed: coords.append((row,col))
        return coords
    
    def is_flagged(self,row,col):
        # return whether a cell at the given coordinates is flagged
        return self.get_cell(row,col).has_flag

    def neighbors(self, row: int, column: int) -> List[Tuple[int, int]]:
        # return valid Moore-neighborhood coordinates (up to eight surrounding cells)
        coords = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, column + dc
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                    coords.append((r, c))
        return coords

    def count_adjacent_mines(self, row: int, column: int) -> int:
        # compute how many of (row, column)’s neighbors contain mines
        return sum(
            1 for r, c in self.neighbors(row, column) 
            if self.grid[r][c].has_mine)

    # sets cell.neighbor_count to num of adjacent mines
    def compute_adjacent_mines(self) -> None:
        # recompute neighbor_count for all cells (useful after manual changes)
        for r in range (self.grid_size):
            for c in range (self.grid_size):
                self.grid[r][c].neighbor_count = self.count_adjacent_mines(r,c)

    #reinits board, does not place mines
    """clear the board to a fresh, mine-free state and update mine_count.
        Mines are not placed here; call place_mines() after the first click."""
    def reset(self, mine_count: int):
        if mine_count > self.grid_size * self.grid_size:
            raise ValueError(" mine_count too large ")
        self.mine_count = mine_count
        # brand-new cells; neighbor counts will be recalculated after placement
        self.grid = [[Cell() for _ in range(self.grid_size)]
                     for _ in range(self.grid_size)]

