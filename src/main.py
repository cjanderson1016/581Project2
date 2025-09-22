"""
File: main.py
Purpose: Entry point for the Minesweeper application. Wires together the core components — BoardManager (board state),
GameLogic (rules), and GameGUI (Tkinter UI) — then starts the Tk event loop.

Flow:
    1) Create BoardManager with fixed grid size (10x10) and initial mine count.
    2) Create GameLogic bound to that BoardManager (defers mines until first click).
    3) Create GameGUI bound to GameLogic (renders grid, handles clicks/flags).
    4) Run the Tkinter main loop.

Inputs: None

Outputs: Launches a Tkinter window that renders the Minesweeper UI.

Author: Sam Kelemen
Created: 2025-09-18
"""

from board_manager import BoardManager
from game_logic import GameLogic
from UI_renderer import GameGUI

if __name__ == "__main__":
    # make a board manager
    board_mgr = BoardManager(grid_size=10, mine_count=15)

    # connect the game logic to the board
    game_logic = GameLogic(board_mgr)

    # hand the logic to the GUI
    gui = GameGUI(game_logic)

    # start Tkinter loop
    gui.run()