from typing import List, Tuple
from board_manager import BoardManager

class GameLogic:
    # Initialize the game's runtime state.
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
        # Increment the count by 1 when placing, −1 when removing
        return 1 if cell.has_flag else -1

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
            #return the detonated coordinate for the UI to render.
            return [(row, col)]

        # Collect every cell that becomes visible from this action.
        newly_revealed = []
        # Reveal clicked cell; if it’s a 0, cascade to neighbors.
        self._flood_reveal(row, col, newly_revealed)

        # All safe cells are revealed, player wins the game
        if self.revealed_safe_cells >= self.total_safe_cells and not self.is_game_over:
            self.is_game_over = True
        return newly_revealed
    
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