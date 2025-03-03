from threading import Thread

from constants import BASE_JEWEL_SCORE
from events import GameEvent, CRUSH_JEWEL_EVENT
from entities import Jewel, Board, Score

class GameEventHandlingError(Exception):
	def __init__(self, event: GameEvent):
		super().__init__(f"Invalid arguments for event {event.name}: {event.args}")

def crush_jewel_event(event: GameEvent, board: Board, score: Score) -> None:
	if len(event.args) < 1:
		raise GameEventHandlingError(event)
	jewels : list[Jewel] = event.args[0]
	summary = {}
	scores = [0 for type in Jewel.JEWEL_TYPES]
	for jewel in jewels:
		if summary.get(jewel.type, None) == None:
			summary[jewel.type] = 0

		summary[jewel.type] += 1
		scores[jewel.type] += BASE_JEWEL_SCORE * (1 + summary[jewel.type] / 20)

	for i in range(len(scores)):
		_score = scores[i]
		if _score == 0:
			continue

		print(_score)
		jewel_type = i
		Thread(target=score.scores[jewel_type].add, args=[_score]).start()

event_handlers = {
	CRUSH_JEWEL_EVENT: crush_jewel_event
}