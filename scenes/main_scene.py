import sys, pygame

from threading import Thread

from constants import Game, Display
from sizes import get_sizes
from abstract import Scene
from scenes import PausedScene
from entities import MoveCounter, Score, Board
from events import GameEventListener
from event_handlers import event_handlers
from singletons import Global

class MainScene(Scene):
	def __init__(self, entities: tuple[MoveCounter, Score, Board]):
		self.move_counter, self.score, self.board = entities
		self.moved = False
		super().__init__([self.move_counter, self.score, self.board])

	def run(self):
		self.__handle_engine_events()
		self.__handle_game_events()
        
		if self.moved:
			Thread(target=self.board.update).start()
			self.moved = False

	def __handle_engine_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self.board.select(mouse_pos)
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = pygame.mouse.get_pos()
				self.board.select(mouse_pos)
			if event.type == pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_ESCAPE]:
					Global.current_scene = PausedScene(self)

			if self.board.can_try_swap():
					self.moved = self.board.swap()

	def __handle_game_events(self):
		event = GameEventListener.listen()
		if event:
			Global.logger.debug(f"Handling event {event.name}")
			event_handlers[event.name](event, self.move_counter, self.board, self.score)

	@staticmethod
	def new():
		sizes = get_sizes()
		width, height = sizes.get_window_size()
		jewel_size = sizes.get_jewel_size()

		Global.logger.debug(f"window_size: {width, height}, jewel_size: {jewel_size}")

		move_counter = MoveCounter((int(width/2), 20), (30, 30))
		score = Score((Display.MARGIN_W, 60), (Game.BOARD_COLS * jewel_size, 120))
		board = Board((Display.MARGIN_W, 200), Game.BOARD_COLS, Game.BOARD_ROWS, jewel_size)

		return MainScene((move_counter, score, board))
		