from pygame import Surface

from entities import Entity

# "Abstract" class to provide an interface for scenes
class Scene():
	def __init__(self, entities: list[Entity]):
		self.entities = entities

	def run(self) -> None:
		raise NotImplementedError("Scene should implement run method")

	def draw(self, surface: Surface) -> None:
		for entity in self.entities:
			entity.draw(surface)
	