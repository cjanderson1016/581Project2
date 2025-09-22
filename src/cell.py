"""
File: cell.py
Purpose:
    Represents a single cell on the Minesweeper board.

Uses:
    - Store state about whether the cell has a mine, flag, or is revealed.
    - Store the number of neighboring mines (0–8).
    - Provide helper methods for updating its state (flagging, unflagging,
      adding/removing a mine).

Inputs:
    - None

Outputs:
    - State changes are in-memory attributes (has_mine, has_flag, etc.).
    - These attributes are later consumed by GameLogic and GameGUI.

Author: Sam Kelemen, Jenny Tsotezo
Created: 2025-09-16
"""

class Cell:
  def __init__(self):
    # Indicates whether this cell contains a mine.
    self.has_mine: bool = False
    # Indicates whether the player has placed a flag on this cell.
    self.has_flag: bool = False
    # Indicates whether the player has revealed (clicked on) this cell.
    self.is_revealed: bool = False
    # Number of mines in the 8 neighboring cells (0–8).
    self.neighbor_count: int = 0

  # Mark this cell as flagged by the player.
  def flag(self):
    # Set the flag state to True.
    self.has_flag = True

  # Remove a flag from this cell.
  def unflag(self):
    # Set the flag state back to False
    self.has_flag = False

  # Add a mine to this cell.
  def add_mine(self):
      # Set the mine state to True.
      self.has_mine = True

  # Remove a mine from this cell
  def remove_mine(self):
    # Set the mine state back to False.
    self.has_mine = False