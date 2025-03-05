from events import GameEvent

class InvalidJewelStateError(Exception):
    def __init__(self, state: int):
        super().__init__(f"Invalid jewel state: {state}")

class GameEventHandlingError(Exception):
	def __init__(self, event: GameEvent):
		super().__init__(f"Invalid arguments for event {event.name}: {event.args}")