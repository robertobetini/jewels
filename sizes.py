import pygame

from constants import Game, Display

current_display_info = pygame.display.Info()

class Sizes:
    def __init__(self, window_w: int, window_h: int , jewel_size: int | float):
        self.__window_w = window_w
        self.__window_h = window_h
        self.__jewel_size = jewel_size

    def get_window_size(self) -> tuple[int, int]:
        return self.__window_w, self.__window_h

    def get_jewel_size(self) -> int:
        return int(self.__jewel_size)

def get_sizes() -> Sizes:
    current_w, current_h = current_display_info.current_w, current_display_info.current_h
    
    top_margin = 200
    bottom_margin = 20

    jewel_size = Display.JEWEL_SIZE
    height = current_h - Display.MARGIN_H
    
    board_h = Game.BOARD_ROWS * jewel_size
    max_board_h = height - (top_margin + bottom_margin)
    if board_h > max_board_h:
        ratio = max_board_h / board_h
        new_jewel_size = jewel_size * ratio
        if new_jewel_size < jewel_size:
            jewel_size = new_jewel_size

    width = int(Game.BOARD_COLS * jewel_size + 2 * Display.MARGIN_W)
    if width > current_w:
        ratio = current_w / width
        width = current_w
        jewel_size *= ratio

    return Sizes(width, height, jewel_size)
