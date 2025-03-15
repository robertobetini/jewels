import sys, pygame

from pygame import Surface

from abstract import Scene
from entities import Entity
from singletons import Global

class PausedScene(Scene):
	def __init__(self, background_scene: Scene, entities: list[Entity]):
		super().__init__(entities)
		self.background_scene = background_scene

	def run(self):
		self.__handle_engine_events()

	def draw(self, surface: Surface):
		self.background_scene.draw(surface)

		width, height = pygame.display.get_surface().get_size()
		background = Surface((width, height))
		background.set_alpha(170)
		background.fill((0, 0, 0))
		surface.blit(background, (0, 0))

		for entity in self.entities:
			entity.draw(surface)

	def __handle_engine_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				print("clicked")
			if event.type == pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_ESCAPE]:
					Global.current_scene = self.background_scene
