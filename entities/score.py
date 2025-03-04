import pygame

from time import sleep
from pygame import Rect, Surface

from constants import Game, Image, Colors
from entities.entity import Entity

PROGRESS_MAP = {
	1: 100,
	2: 160,
	3: 250,
	4: 390,
	5: 540
}

class Progress:
	def __init__(self):
		self.current = 0.
		self.level = 0
		self.max = 0.
		self.level_up()

	def __repr__(self) -> str:
		progress = int((self.current / self.max) * 10)
		return f"LVL {self.level} [{progress * '='}{(10 - progress) * ' '}] {self.current} / {self.max}"

	def level_up(self) -> None:
		self.level += 1
		remaining = self.current - self.max
		self.current = 0
		self.max = PROGRESS_MAP[self.level]

		if remaining > 0:
			self.add(remaining)

	def add(self, amount: int | float, delta: float = 0.005) -> None:
		target = self.current + amount
		updates = 30
		for _ in range(updates - 1):
			amount = (target - self.current) / 10
			if abs(self.current + amount) >= target:
				break
			self.current += amount
			sleep(delta)

		self.current = target
		if self.current >= self.max:
			self.level_up()

	def get_percentage(self) -> float:
		return min(self.current / self.max, 1)
	

class Score(Entity):
	def __init__(self, pos: tuple[int, int], size = (20, 20)):
		super().__init__(pos, size, (110, 118, 113, 0))

		self.scores = [ Progress() for jewel_type in Game.JEWEL_TYPES ]
		self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

	def __repr__(self) -> str:
		repr = ""
		for score in self.scores:
			repr += f"{score}\n"
		return repr

	def draw(self, surface: Surface) -> None:
		self.draw_brackground(surface, 60)

		width, height = self.size
		portion_x, portion_y = width / 3, height / 3
		offset_x, offset_y = self.pos
		margin = 10

		for i in range(len(self.scores)):
			# draw icon
			pos = int((i % 3) * portion_x + offset_x + margin), int((i // 3) * portion_y + offset_y + margin)
			jewel_type = i
			image = Image.JEWEL_ICONS[jewel_type]
			surface.blit(image, pos)

			# draw progress
			progress = self.scores[i]
			max_progress = portion_x - 70
			target = progress.get_percentage() * max_progress
			progress_pos = pos[0] + image.get_width() + 10, pos[1]

			current_rect = Rect(progress_pos, (progress.get_percentage() * max_progress, image.get_width()))
			max_rect = Rect(progress_pos, (max_progress, image.get_width()))
			pygame.draw.rect(surface, Colors.JEWEL_PROGRESS_GAUGE_COLOR, current_rect)
			pygame.draw.rect(surface, self.color, max_rect, 3)

			# text display
			text = self.font.render(str(progress.level), True, Colors.JEWEL_PROGRESS_GAUGE_COLOR)
			surface.blit(text, (pos[0] + max_rect.width + 32, pos[1] - 1))
