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
		self.size = (200, height)
		self.surface = Surface(self.size)
		self.surface.set_alpha(230)
		self.surface.blit(self.rendered_text, (2, 2))

	def draw(self, surface: Surface) -> None:
		super().draw_brackground(surface, 230, 2, (35, 40, 85))
		surface.blit(self.surface, self.pos)

	def is_clicked(self, pos: tuple[int, int] | tuple[float, float]) -> bool:
		x, y = pos
		button_x, button_y = self.pos
		button_w, button_h = self.size

		if x < button_x or x > button_x + button_w:
			return False
		if y < button_y or y > button_y + button_h:
			return False

		return True
