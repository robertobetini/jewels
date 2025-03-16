event_queue = []

CRUSH_JEWEL_EVENT = "CRUSH_JEWEL_EVENT"
MOVE_JEWEL_EVENT = "MOVE_JEWEL_EVENT"
OUT_OF_MOVES_EVENT = "OUT_OF_MOVES_EVENT"
JEWEL_SELECTED_EVENT = "JEWEL_SELECTED_EVENT"
RESTART_GAME_EVENT = "RESTAR_GAME_EVENT"
BACK_TO_TITLE_EVENT = "BACK_TO_TITLE_EVENT"

class GameEvent():
	def __init__(self, name: str, args: list = []):
		self.name = name
		self.args = args

class GameEventEmitter():
	@staticmethod
	def emit(event: GameEvent) -> None:
		event_queue.append(event)

class GameEventListener():
	@staticmethod
	def listen() -> GameEvent | None:
		if event_queue:
			return event_queue.pop(0)
		else:
			return None

