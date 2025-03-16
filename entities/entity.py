import pygame

from pygame import Surface, Rect

class Entity:
	def __init__(self, pos: tuple[int, int], size: tuple[int, int] = (20, 20), color: tuple[int, int, int] | tuple[int, int, int, int] = (0, 0, 0)):
		self.pos = pos
		self.color = color
		self.size = size

	def draw(self, surface: Surface) -> None:
		x, y = self.pos
		width, height = self.size
		rect = Rect(x, y, width, height)
		pygame.draw.rect(surface, self.color, rect, width=1)

	def draw_brackground(self, surface, alpha: int = 255, thickness: int = 5, color: tuple[int, int, int] | None = None):
		background = Surface(self.size)
		background.set_alpha(alpha)
		background.fill(color if color else (0, 0, 0))
		surface.blit(background, self.pos)

		background_border = Rect(self.pos, self.size)
		pygame.draw.rect(surface, self.color, background_border, thickness)