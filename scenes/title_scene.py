import sys, pygame

from pygame import Surface
from pygame.font import Font, get_default_font

from events import *

from constants import Text, Colors
from abstract import Scene
from entities.gui import Button
from scenes.main_scene import MainScene
from singletons import Global

class TitleScene(Scene):
	def __init__(self):
		self.resume_button = Button((100, 500), "NEW GAME")
		self.exit_button = Button((100, 600), "EXIT")
		self.buttons : list[Button] = [ self.resume_button, self.exit_button ]

		super().__init__([self.resume_button, self.exit_button])

		self.font = Font(get_default_font(), Text.GUI_TEXT_SIZE)
		self.click_action = ""

		width, height = pygame.display.get_surface().get_size()
		
		self.background_surface = Surface((width, height))
		self.background_surface.fill(Colors.BACKGROUND_COLOR)

		self.left_brackground_surface = Surface((400, height))
		self.left_brackground_surface.set_alpha(200)
		self.left_brackground_surface.fill((0, 0, 0))

		self.title_text = self.font.render("JEWELS", True, Colors.GUI_TEXT_COLOR)

		# highlight button if mouse is already overlapping when scene is first disaplayed
		self.__update_button_highlight()

	def run(self):
		self.__handle_engine_events()

	def draw(self, surface: Surface):
		surface.blit(self.background_surface, (0, 0))
		surface.blit(self.left_brackground_surface, (0, 0))
		surface.blit(self.title_text, (100, 100))

		for entity in self.entities:
			entity.draw(surface)

	def __update_button_highlight(self):
		mouse_pos = pygame.mouse.get_pos()
		for button in self.buttons:
			if button.is_overlapped(mouse_pos):
				button.highlighted = True
			else:
				button.highlighted = False

	def __start(self):
		Global.current_scene = MainScene.new()

	def __exit(self):
		sys.exit()

	def __handle_engine_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.__exit()

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
					if self.click_action == "NEW GAME":
						self.__start()
					elif self.click_action == "EXIT":
						self.__exit()

			