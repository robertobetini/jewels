import pygame

from pygame import Surface
from pygame.event import Event

from events import *

from constants import Text
from abstract import Scene, MenuScene
from entities.gui import Button
from singletons import Global

class PausedScene(MenuScene):
	def __init__(self, background_scene: Scene):
		self.resume_button = Button((100, 300), Text.RESUME_BUTTON_TEXT)
		self.restart_button = Button((100, 400), Text.RESTART_BUTTON_TEXT)
		self.back_to_title_button = Button((100, 500), Text.BACK_TO_TITLE_BUTTON_TEXT)
		self.exit_button = Button((100, 600), Text.EXIT_BUTTON_TEXT)
		super().__init__(Text.PAUSED_MENU_HEADER, [self.resume_button, self.restart_button, self.back_to_title_button, self.exit_button])

		self.background_scene = background_scene

	def __resume(self):
		Global.current_scene = self.background_scene

	def __restart(self):
		game_event = GameEvent(RESTART_GAME_EVENT)
		GameEventEmitter.emit(game_event)
		Global.current_scene = self.background_scene

	def __go_back_to_title(self):
		from scenes import TitleScene
		Global.current_scene = TitleScene()

	def _handle_engine_events(self) -> list[Event]:
		events = super()._handle_engine_events()

		for event in events:
			if event.type == pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_ESCAPE]:
					self.__resume()

		return events

	def _handle_click_action(self) -> None:
		if self.click_action == Text.RESUME_BUTTON_TEXT:
			self.__resume()
		elif self.click_action == Text.RESTART_BUTTON_TEXT:
			self.__restart()
		elif self.click_action == Text.BACK_TO_TITLE_BUTTON_TEXT:
			self.__go_back_to_title()
		elif self.click_action == Text.EXIT_BUTTON_TEXT:
			self._exit()

	def draw(self, surface: Surface) -> None:
		self.background_scene.draw(surface)
		super().draw(surface)
		