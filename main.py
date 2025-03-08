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
    screen.fill(background_color)

    for entity in entities:
        entity.draw(surface)

if __name__ == "__main__":
    current_display_info = pygame.display.Info()

    # print(current_display)

    background_color = Colors.BACKGROUND_COLOR
    horizontal_margin = 50
    vertical_margin = 100
    board_cols, board_rows = 12, 10
    width = board_cols * Display.JEWEL_SIZE + 2 * horizontal_margin

    move_counter = MoveCounter((int(width/2), 20), (30, 30))
    score = Score((horizontal_margin, 60), (board_cols * Display.JEWEL_SIZE, 120))
    board = Board((horizontal_margin, 200), board_cols, board_rows)
    moved = False
    height = board_rows * Display.JEWEL_SIZE + move_counter.size[1] + score.size[1] + vertical_margin

    size = width, min(current_display_info.current_h, Display.MAX_WINDOW_HEIGHT) - vertical_margin
    screen = pygame.display.set_mode(size)

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
