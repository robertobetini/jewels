import sys, pygame

from threading import Thread
from pygame import Surface

from entities import Entity, Board, Score
from events import GameEventListener
from event_handlers import event_handlers

def handle_engine_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            selected = board.select(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            selected = board.select(mouse_pos)

            if board.can_try_swap():
                global moved
                moved = board.swap()

def handle_game_events():
    event = GameEventListener.listen()
    if event:
        event_handlers[event.name](event, board, score)


def draw(surface: Surface, entities: list[Entity]):
    screen.fill(background_color)

    for entity in entities:
        entity.draw(surface)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    background_color = 100, 110, 95
    horizontal_margin = 50
    rows, cols = 6, 6
    board = Board((horizontal_margin, 160), rows, cols)
    content_width = board.width * board.cell_size 
    score = Score((horizontal_margin, 20), (content_width, 120))
    moved = False

    size = width, height = content_width + 2 * horizontal_margin, board.width * board.cell_size + board.pos[1] + score.pos[1]
    screen = pygame.display.set_mode(size)

    while True:
        handle_engine_events()
        handle_game_events()
        draw(screen, [score, board])
        
        if moved:
            Thread(target=board.update).start()
            moved = False

        pygame.display.flip()
