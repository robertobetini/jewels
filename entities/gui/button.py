import pygame

from time import sleep
from threading import Thread

from pygame import Surface
from pygame.font import Font, get_default_font

from constants import Text, Colors
from entities import Entity

class Button(Entity):
	def __init__(self, pos: tuple[int, int], text: str):
		super().__init__(pos, (200, 50), Colors.GUI_TEXT_COLOR)

		self.font = Font(get_default_font(), Text.GUI_TEXT_SIZE)
		self.text = text
		self.rendered_text = self.font.render(self.text, True, self.color)
		_, height = self.rendered_text.get_size()
		self.size = (250, height)
		self.surface = Surface(self.size, pygame.SRCALPHA, 32)
		self.surface.set_alpha(220)
		self.surface.blit(self.rendered_text, (2, 2))

		self.highlighted = False
		self.highlighted_background = Surface(self.size)
		self.highlighted_background.set_alpha(127)
		self.highlighted_background.fill((105, 120, 113))

		self.alpha = 0

	def draw(self, surface: Surface) -> None:
		surface.blit(self.surface, self.pos)
		if self.highlighted:
			surface.blit(self.highlighted_background, self.pos)

	def is_overlapped(self, pos: tuple[int, int] | tuple[float, float]) -> bool:
		x, y = pos
		button_x, button_y = self.pos
		button_w, button_h = self.size

		if x < button_x or x > button_x + button_w:
			return False
		if y < button_y or y > button_y + button_h:
			return False

		return True

	def highlight(self):
		def __highlight(button):
			button.highlighted = True

			button.alpha = 0
			while button.highlighted and button.alpha < 127:
				button.highlighted_background.set_alpha(button.alpha)
				button.alpha += 15
				sleep(0.01)

		Thread(target=__highlight, args=(self,)).start()

	def unhighlight(self):
		def __unhighlight(button):
			while button.alpha > 0:
				button.highlighted_background.set_alpha(button.alpha)
				button.alpha -= 10
				sleep(0.06)

			button.alpha = 0
			button.highlighted_background.set_alpha(button.alpha)
			button.highlighted = False

		Thread(target=__unhighlight, args=(self,)).start()
