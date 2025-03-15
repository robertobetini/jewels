import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from pygame import Surface

from constants import Colors
from entities.scenes import Scene, MainScene
from entities import Board, Score, MoveCounter
from sizes import init_sizes

current_scene : Scene | None = None

def draw(surface: Surface, scene: Scene):
    screen.fill(Colors.BACKGROUND_COLOR)
    scene.draw(surface)

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

    screen = pygame.display.set_mode(sizes.get_window_size())
    current_scene = MainScene((move_counter, score, board))

    while True:
        current_scene.run()
        draw(screen, current_scene)
        pygame.display.flip()
