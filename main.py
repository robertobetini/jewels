import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from pygame import Surface

from constants import Colors, Game, Display
from abstract import Scene
from scenes import MainScene
from entities import Board, Score, MoveCounter
from sizes import get_sizes
from singletons import Global

def draw(surface: Surface, scene: Scene):
    screen.fill(Colors.BACKGROUND_COLOR)
    scene.draw(surface)

if __name__ == "__main__":
    sizes = get_sizes()
    width, height = sizes.get_window_size()
    jewel_size = sizes.get_jewel_size()

    print(f"window_size: {width, height}, jewel_size: {jewel_size}")

    move_counter = MoveCounter((int(width/2), 20), (30, 30))
    score = Score((Display.MARGIN_W, 60), (Game.BOARD_COLS * jewel_size, 120))
    board = Board((Display.MARGIN_W, 200), Game.BOARD_COLS, Game.BOARD_ROWS, jewel_size)

    screen = pygame.display.set_mode(sizes.get_window_size())
    Global.current_scene = MainScene((move_counter, score, board))

    while True:
        Global.current_scene.run()
        draw(screen, Global.current_scene)
        pygame.display.flip()
