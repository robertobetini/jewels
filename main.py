import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

from pygame import Surface

from constants import Colors
from abstract import Scene
from sizes import get_sizes
from scenes import TitleScene
from singletons import Global

def draw(surface: Surface, scene: Scene):
    screen.fill(Colors.BACKGROUND_COLOR)
    scene.draw(surface)

if __name__ == "__main__":
    sizes = get_sizes()
    screen = pygame.display.set_mode(sizes.get_window_size())

    Global.current_scene = TitleScene()
    while True:
        if Global.current_scene:
            Global.current_scene.run()
            draw(screen, Global.current_scene)
            pygame.display.flip()
