import pygame

from pygame import Surface

from constants import Game
from entities.entity import Entity
from events import GameEvent, GameEventEmitter, OUT_OF_MOVES_EVENT

class MoveCounter(Entity):
	def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
		super().__init__(pos, size)

		self.count = Game.STARTING_MOVES
		self.font = pygame.font.Font(pygame.font.get_default_font(), 32)

	def draw(self, surface: Surface) -> None:
		text = self.font.render(str(self.count), True, self.color)
		surface.blit(text, self.pos)

	def decrease(self, amount: int) -> None:
		self.count -= amount

		if self.count < 1 :
			event = GameEvent(OUT_OF_MOVES_EVENT)
			GameEventEmitter.emit(event)