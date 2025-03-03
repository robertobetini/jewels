event_queue = []

CRUSH_JEWEL_EVENT = "CRUSH_JEWEL_EVENT"

class GameEvent():
	def __init__(self, name: str, args: list = []):
		self.name = name
		self.args = args

class GameEventEmitter():
	def __init__(self, queue: list[GameEvent]):
		self.queue = queue

	@staticmethod
	def emit(event: GameEvent) -> None:
		event_queue.append(event)

class GameEventListener():
	def __init__(self, queue: list[GameEvent]):
		self.queue = queue

	@staticmethod
	def listen() -> GameEvent | None:
		if len(event_queue) > 0:
			return event_queue.pop(0)
		else:
			return None

