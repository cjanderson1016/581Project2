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