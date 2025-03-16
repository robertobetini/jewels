from constants import Text
from abstract import MenuScene
from entities.gui import Button
from scenes.main_scene import MainScene
from singletons import Global

class TitleScene(MenuScene):
	def __init__(self):
		self.resume_button = Button((100, 500), Text.NEW_GAME_BUTTON_TEXT)
		self.exit_button = Button((100, 600), Text.EXIT_BUTTON_TEXT)
		super().__init__(Text.TITLE_MENU_HEADER, [self.resume_button, self.exit_button])

	def __start(self) -> None:
		Global.current_scene = MainScene.new()

	def _handle_click_action(self) -> None:
		if self.click_action == Text.NEW_GAME_BUTTON_TEXT:
			self.__start()
		elif self.click_action == Text.EXIT_BUTTON_TEXT:
			self._exit()
			