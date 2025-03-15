import sys, pygame

from threading import Thread
from pygame import Surface

from entities.scenes.scene import Scene
from entities import MoveCounter, Score, Board
from events import GameEventListener
from event_handlers import event_handlers

moved = False

class MainScene(Scene):
	def __init__(self, entities: tuple[MoveCounter, Score, Board]):
		self.move_counter, self.score, self.board = entities
		self.moved = False

		super().__init__([self.move_counter, self.score, self.board])

	def run(self):
		self.handle_engine_events()
		self.handle_game_events()
        
		self.moved
		if self.moved:
			Thread(target=self.board.update).start()
			self.moved = False

	def handle_engine_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self.board.select(mouse_pos)
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = pygame.mouse.get_pos()
				self.board.select(mouse_pos)

			if self.board.can_try_swap():
					self.moved = self.board.swap()

	def handle_game_events(self):
		event = GameEventListener.listen()
		if event:
			print(f"Handling event {event.name}")
			event_handlers[event.name](event, self.move_counter, self.board, self.score)

	def draw(self, surface: Surface):
		for entity in self.entities:
			entity.draw(surface)