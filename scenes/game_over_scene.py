from pygame import Surface

from events import *

from constants import Text
from abstract import Scene, MenuScene
from entities.gui import Button
from singletons import Global

class GameOverScene(MenuScene):
	def __init__(self, background_scene: Scene):
		self.restart_button = Button((100, 400), Text.RESTART_BUTTON_TEXT)
		self.back_to_title_button = Button((100, 500), Text.BACK_TO_TITLE_BUTTON_TEXT)
		self.exit_button = Button((100, 600), Text.EXIT_BUTTON_TEXT)
		super().__init__(Text.GAME_OVER_MENU_HEADER, [self.restart_button, self.back_to_title_button, self.exit_button])

		self.background_scene = background_scene

	def __restart(self) -> None:
		game_event = GameEvent(RESTART_GAME_EVENT)
		GameEventEmitter.emit(game_event)
		Global.current_scene = self.background_scene

	def __go_back_to_title(self) -> None:
		from scenes import TitleScene
		Global.current_scene = TitleScene()

	def _handle_click_action(self) -> None:
		if self.click_action == Text.RESTART_BUTTON_TEXT:
			self.__restart()
		elif self.click_action == Text.BACK_TO_TITLE_BUTTON_TEXT:
			self.__go_back_to_title()
		elif self.click_action == Text.EXIT_BUTTON_TEXT:
			self._exit()

	def draw(self, surface: Surface) -> None:
		self.background_scene.draw(surface)
		super().draw(surface)
