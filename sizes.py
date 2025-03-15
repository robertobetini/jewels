import pygame

from constants import Display

SIZES = None

class Sizes:
    def __init__(self, window_w: int, window_h: int , jewel_size: int | float):
        self.__window_w = window_w
        self.__window_h = window_h
        self.__jewel_size = jewel_size

    def get_window_size(self) -> tuple[int, int]:
        return self.__window_w, self.__window_h

    def get_jewel_size(self) -> int:
        return int(self.__jewel_size)

def init_sizes(cols: int, rows: int, margin_w: int, margin_h: int) -> Sizes:
    current_display_info = pygame.display.Info()
    current_w, current_h = current_display_info.current_w, current_display_info.current_h
    top_margin = 200
    bottom_margin = 20

    jewel_size = Display.JEWEL_SIZE
    height = current_h - margin_h
    
    board_h = rows * jewel_size
    max_board_h = height - (top_margin + bottom_margin)
    if board_h > max_board_h:
        ratio = max_board_h / board_h
        new_jewel_size = jewel_size * ratio
        if new_jewel_size < jewel_size:
            jewel_size = new_jewel_size

    width = int(cols * jewel_size + 2 * margin_w)
    if width > current_w:
        ratio = current_w / width
        width = current_w
        jewel_size *= ratio

    SIZES = Sizes(width, height, jewel_size)
    return SIZES
