import sys, pygame

from pygame import Surface
from pygame.event import Event
from pygame.font import Font, get_default_font

from constants import Text, Colors
from abstract import Scene
from entities.gui.button import Button

class MenuScene(Scene):
	def __init__(self, header_text: str, buttons: list[Button]):
		super().__init__(list(buttons))

		self.buttons = buttons
		self.font = Font(get_default_font(), Text.GUI_TEXT_SIZE)
		self.click_action = ""
		self.second_click_action = ""

		width, height = pygame.display.get_surface().get_size()

		self.background_surface = Surface((width, height))
		self.background_surface.set_alpha(Colors.MENU_BACKGROUND_PRYMARY_COLOR_ALPHA)
		self.background_surface.fill(Colors.MENU_BACKGROUND_PRIMARY_COLOR)

		self.left_brackground_surface = Surface((400, height))
		self.left_brackground_surface.set_alpha(Colors.MENU_BACKGROUND_SECONDARY_COLOR_ALPHA)
		self.left_brackground_surface.fill(Colors.MENU_BACKGROUND_SECONDARY_COLOR)

		self.header = self.font.render(header_text, True, Colors.GUI_TEXT_COLOR)
		self.header.set_alpha(Colors.MENU_BACKGROUND_SECONDARY_COLOR_ALPHA)

		# highlight button if mouse is already overlapping when scene is first disaplayed
		self.__update_button_highlight()

	def __update_button_highlight(self) -> None:
		mouse_pos = pygame.mouse.get_pos()

		for button in self.buttons:
			if button.is_overlapped(mouse_pos):
				if button.highlighted:
					break
				button.highlight()
			else:
				button.unhighlight()

	def _handle_engine_events(self) -> list[Event]:
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				self._exit()

			elif event.type == pygame.MOUSEMOTION:
				self.__update_button_highlight()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				
				self.click_action = ""
				for button in self.buttons:
					if button.is_overlapped(mouse_pos):
						self.click_action = button.text
						break

			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = pygame.mouse.get_pos()

				click_action = ""
				for button in self.buttons:
					if button.is_overlapped(mouse_pos):
						click_action = button.text
						break

				# if mouse is up on a different button, ignore action
				if self.click_action == click_action:
					self._handle_click_action()

		return events

	def _exit(self) -> None:
		sys.exit()

	def _handle_click_action(self) -> None:
		raise NotImplementedError("This method should be implemented to handle button click")

	def draw(self, surface: Surface) -> None:
		surface.blit(self.background_surface, (0, 0))
		surface.blit(self.left_brackground_surface, (0, 0))
		surface.blit(self.header, (100, 100))

		for entity in self.entities:
			entity.draw(surface)

	def run(self) -> None:
		self._handle_engine_events()
