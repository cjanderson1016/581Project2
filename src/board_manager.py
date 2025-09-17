from typing import List
from cell import Cell
import random

class BoardManager:
  def __init__(self, grid_size: int, mine_count: int):
    self.grid = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
    self.mine_count = mine_count

  def place_mines(self):
    rows = len(self.grid)
    cols = len(self.grid[0])
    all_coords = [(r, c) for r in range(rows) for c in range(cols)]
    mine_coords = random.sample(all_coords, self.mine_count)
    for r, c in mine_coords:
      self.grid[r][c].has_mine = True

  def get_cell(self, row: int, column: int):
    return self.grid[row][column]

  def neighbors(self, row: int, column: int) -> List[Cell]:
    neighbor_cells = []
    rows = len(self.grid)
    cols = len(self.grid[0])

    for dr in [-1, 0, 1]:
      for dc in[-1, 0, 1]:
        if dr == 0 and dc == 0:
          continue
        r, c = row + dr, column + dc
        if 0 <= r < rows and 0 <= c < cols:
          neighbor_cells.append(self.grid[r][c])

    return neighbor_cells

  def count_adjacent_mines(self, row: int, column: int) -> int:
    neighbor_mines = 0
    rows = len(self.grid)
    cols = len(self.grid[0])

    for dr in [-1, 0, 1]:
      for dc in[-1, 0, 1]:
        if dr == 0 and dc == 0:
          continue
        r, c = row + dr, column + dc
        if 0 <= r < rows and 0 <= c < cols:
          if self.grid[r][c].has_mine:
            neighbor_mines += 1
    return neighbor_mines

  def reset(self, mine_count: int):
    pass  