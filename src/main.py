from board_manager import BoardManager
from game_logic import GameLogic
from UI_renderer import GameGUI

if __name__ == "__main__":
    # make a board manager
    gui = GameGUI()
    # start Tkinter loop
    gui.run()