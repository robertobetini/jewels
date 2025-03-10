import sys, pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from threading import Thread
from pygame import Surface

from constants import Display, Colors
from entities import Entity, Board, Score, MoveCounter
from events import GameEventListener
from event_handlers import event_handlers

class Sizes:
    def __init__(self, window_w: int, window_h: int , jewel_size: int | float):
        self.__window_w = window_w
        self.__window_h = window_h
        self.__jewel_size = jewel_size

    def get_window_size(self) -> tuple[int, int]:
        return self.__window_w, self.__window_h

    def get_jewel_size(self) -> int:
        return int(self.__jewel_size)

def calculate_sizes(cols: int, rows: int, margin_w: int, margin_h: int) -> Sizes:
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

    return Sizes(width, height, jewel_size)

def handle_engine_events(board: Board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            board.select(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            board.select(mouse_pos)

            if board.can_try_swap():
                global moved
                moved = board.swap()

def handle_game_events(move_counter: MoveCounter, score: Score, board: Board):
    event = GameEventListener.listen()
    if event:
        print(f"Handling event {event.name}")
        event_handlers[event.name](event, move_counter, board, score)

def draw(surface: Surface, entities: list[Entity]):
    screen.fill(Colors.BACKGROUND_COLOR)

    for entity in entities:
        entity.draw(surface)

if __name__ == "__main__":
    margin_w, margin_h = 50, 100
    board_cols, board_rows = 20, 20

    sizes = calculate_sizes(board_cols, board_rows, margin_w, margin_h)
    width, height = sizes.get_window_size()
    jewel_size = sizes.get_jewel_size()

    print(f"window_size: {width, height}, jewel_size: {jewel_size}")

    move_counter = MoveCounter((int(width/2), 20), (30, 30))
    score = Score((margin_w, 60), (board_cols * jewel_size, 120))
    board = Board((margin_w, 200), board_cols, board_rows, jewel_size)
    moved = False

    screen = pygame.display.set_mode(sizes.get_window_size())

    while True:
        if board.finished:
            raise Exception("Game Over")

        handle_engine_events(board)
        handle_game_events(move_counter, score, board)
        draw(screen, [move_counter, score, board])
        
        if moved:
            Thread(target=board.update).start()
            moved = False

        pygame.display.flip()
