from typing import List, Tuple
from board_manager import BoardManager

class GameLogic:
    def __init__(self, board_mgr: BoardManager):
        self.board_mgr = board_mgr
        self.is_first_click: bool = True
        self.is_game_over: bool = False
        self.revealed_safe_cells: int = 0
        self.total_safe_cells: int = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count
        self.flags_placed: int = 0

    def reset_game(self, mine_count: int):
        self.board_mgr.reset(mine_count)
        self.is_first_click = True
        self.is_game_over = False
        self.revealed_safe_cells = 0
        self.flags_placed = 0
        self.total_safe_cells = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count

    def toggle_flag(self, row: int, col: int) -> int:
        if self.is_game_over:
            return 0
        cell = self.board_mgr.get_cell(row, col)
        if cell.is_revealed:
            return 0
        if not cell.has_flag and self.flags_placed >= self.board_mgr.mine_count:
            return 0
        cell.has_flag = not cell.has_flag
        self.flags_placed += 1 if cell.has_flag else -1
        return 1 if cell.has_flag else -1

    def reveal_cell(self, row: int, col: int) -> List[Tuple[int, int]]:
        if self.is_game_over:
            return []
        cell = self.board_mgr.get_cell(row, col)
        if cell.is_revealed or cell.has_flag:
            return []

        if self.is_first_click:
            self.board_mgr.place_mines(row, col)
            self.total_safe_cells = self.board_mgr.grid_size ** 2 - self.board_mgr.mine_count
            self.is_first_click = False

        if cell.has_mine:
            self.is_game_over = True
            return [(row, col)]

        newly_revealed = []
        self._flood_reveal(row, col, newly_revealed)

        if self.revealed_safe_cells >= self.total_safe_cells and not self.is_game_over:
            self.is_game_over = True
        return newly_revealed
    
    def _flood_reveal(self, row: int, col: int, out_list: List[Tuple[int, int]]):
        stack = [(row, col)]
        visited = set()
    
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
    
            cell = self.board_mgr.get_cell(r, c)
            if cell.is_revealed or cell.has_flag or cell.has_mine:
                continue
    
            cell.is_revealed = True
            self.revealed_safe_cells += 1
            out_list.append((r, c))
    
            if cell.neighbor_count == 0:
                for nr, nc in self.board_mgr.neighbors(r, c):
                    ncell = self.board_mgr.get_cell(nr, nc)
                    if not ncell.is_revealed and not ncell.has_flag and not ncell.has_mine:
                        stack.append((nr, nc))

