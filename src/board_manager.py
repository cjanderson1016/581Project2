from typing import List
from cell import Cell
import random

class BoardManager:
    def __init__(self, grid_size: int, mine_count: int):
        if grid_size <= 0:
            raise ValueError("grid_size must be positive")
        if mine_count > grid_size * grid_size:
            raise ValueError("mine_count cannot exceed total number of cells")

        self.grid_size = grid_size
        self.mine_count = mine_count
        self.grid = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

    def place_mines(self):
        rows = len(self.grid)
        cols = len(self.grid[0])
        all_coords = [(r, c) for r in range(rows) for c in range(cols)]
        mine_coords = random.sample(all_coords, self.mine_count)
        for r, c in mine_coords:
            self.grid[r][c].has_mine = True

    def get_cell(self, row: int, column: int):
        if not (0 <= row < self.grid_size and 0 <= column < self.grid_size):
            raise IndexError("cell coordinates out of range")
        return self.grid[row][column]

    def neighbors(self, row: int, column: int) -> List[Cell]:
        neighbor_cells = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, column + dc
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                    neighbor_cells.append(self.grid[r][c])
        return neighbor_cells

    def count_adjacent_mines(self, row: int, column: int) -> int:
        return sum(1 for cell in self.neighbors(row, column) if cell.has_mine)

    def reset(self, mine_count: int):
        pass  
