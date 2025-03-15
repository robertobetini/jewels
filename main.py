import sys, pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from threading import Thread
from pygame import Surface

from constants import Colors
from entities import Entity, Board, Score, MoveCounter
from events import GameEventListener
from event_handlers import event_handlers
from sizes import init_sizes

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

    sizes = init_sizes(board_cols, board_rows, margin_w, margin_h)
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
