from entities.entity import Entity

# "Abstract" class to provide an interface for scenes
class Scene(Entity):
	def __init__(self, entities: list[Entity]):
		self.entities = entities

	def run(self) -> None:
		raise NotImplemented()