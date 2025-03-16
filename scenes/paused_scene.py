import sys, pygame

from pygame import Surface
from pygame.font import Font, get_default_font

from constants import Text, Colors
from abstract import Scene
from events import GameEvent, GameEventEmitter, RESTART_GAME_EVENT
from entities import Entity
from entities.gui import Button
from singletons import Global

class PausedScene(Scene):
	def __init__(self, background_scene: Scene, entities: list[Entity]):
		self.resume_button = Button((100, 300), "RESUME")
		self.restart_button = Button((100, 400), "RESTART")
		self.exit_button = Button((100, 500), "EXIT")

		super().__init__([self.resume_button, self.restart_button, self.exit_button])
		self.background_scene = background_scene
		self.font = Font(get_default_font(), Text.GUI_TEXT_SIZE)

	def run(self):
		self.__handle_engine_events()

	def draw(self, surface: Surface):
		self.background_scene.draw(surface)

		width, height = pygame.display.get_surface().get_size()

		background = Surface((width, height))
		background.set_alpha(80)
		background.fill((110, 127, 150))
		surface.blit(background, (0, 0))

		left_brackground = Surface((400, height))
		left_brackground.set_alpha(200)
		left_brackground.fill((0, 0, 0))
		surface.blit(left_brackground, (0, 0))

		text = self.font.render("PAUSED", True, Colors.GUI_TEXT_COLOR)
		surface.blit(text, (100, 100))

		for entity in self.entities:
			entity.draw(surface)

	def __handle_engine_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				
				if self.resume_button.is_clicked(mouse_pos):
					Global.current_scene = self.background_scene
				elif self.restart_button.is_clicked(mouse_pos):
					game_event = GameEvent(RESTART_GAME_EVENT)
					GameEventEmitter.emit(game_event)
					Global.current_scene = self.background_scene
				elif self.exit_button.is_clicked(mouse_pos):
					sys.exit()

			if event.type == pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_ESCAPE]:
					Global.current_scene = self.background_scene
