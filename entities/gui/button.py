import pygame

from pygame import Surface
from pygame.font import Font, get_default_font

from constants import Text, Colors
from entities import Entity

class Button(Entity):
	def __init__(self, pos: tuple[int, int], text: str):
		self.font = Font(get_default_font(), Text.GUI_TEXT_SIZE)
		self.text = text

		super().__init__(pos, (200, 50), Colors.GUI_TEXT_COLOR)

	def draw(self, surface: Surface) -> None:
		super().draw(surface)
		text = self.font.render(self.text, True, self.color)
		surface.blit(text, self.pos)
