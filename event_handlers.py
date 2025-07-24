from threading import Thread

from events import *

from constants import Game
from errors import GameEventHandlingError
from entities import Jewel, Board, Score, MoveCounter
from singletons import Global

def crush_jewel_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	if len(event.args) != 2:
		raise GameEventHandlingError(event)

	jewels: list[Jewel] = event.args[0]
	updates_in_a_row: int = event.args[1]

	summary = {}
	scores = [0 for _ in Game.JEWEL_TYPES]
	for jewel in jewels:
		if summary.get(jewel.type, None) == None:
			summary[jewel.type] = 0

		summary[jewel.type] += 1
		scores[jewel.type] += int(Game.BASE_JEWEL_SCORE * (1 + summary[jewel.type] * 0.05) ** updates_in_a_row)

	for i in range(len(scores)):
		_score = scores[i]
		if _score == 0:
			continue

		jewel_type = i
		Thread(target=score.scores[jewel_type].add, args=[_score]).start()

def move_jewel_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	Thread(target=move_counter.decrease, args=[1]).start()

def out_of_moves_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	from scenes import TitleScene
	board.game_over()

def jewel_selected_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	pass

def jewel_deselected_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	pass

def jewel_level_up_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	pass

def restart_game_event(event: GameEvent, move_counter: MoveCounter, board: Board, score: Score) -> None:
	from scenes import MainScene
	Global.current_scene = MainScene.new()

event_handlers = {
	CRUSH_JEWEL_EVENT: crush_jewel_event,
	MOVE_JEWEL_EVENT: move_jewel_event,
	OUT_OF_MOVES_EVENT: out_of_moves_event,
	JEWEL_SELECTED_EVENT: jewel_selected_event,
	RESTART_GAME_EVENT: restart_game_event,
	JEWEL_DESELECTED_EVENT: jewel_deselected_event,
	JEWEL_LEVEL_UP_EVENT: jewel_level_up_event
}