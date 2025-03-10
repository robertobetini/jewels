import pygame

from time import sleep
from random import randint, choice
from threading import Thread
from pygame import Surface

from entities.entity import Entity
from entities.jewel import Jewel, JEWEL_CRUSHED, JEWEL_IDLE, JEWEL_MOVING
from constants import Display, Game, Sound, Colors

from events import GameEvent, GameEventEmitter, CRUSH_JEWEL_EVENT, MOVE_JEWEL_EVENT

def lock_board(func):
	def wrapper(self, *args):
		self.locked = True
		func(self, *args)
		self.locked = False

	return wrapper

def clear_selected(func):
	def wrapper(self) -> bool:
		swapped = func(self)
		for jewel in self.selected:
			if jewel:
				jewel.highlighted = False
				
		self.selected = []
		return swapped

	return wrapper

class Board(Entity):
	def __init__(self, pos: tuple[int, int], width: int, height: int, cell_size: int):
		self.cell_size = cell_size
		size = self.cell_size * width, self.cell_size * height
		super().__init__(pos, size, Colors.BORDER_COLOR)
		
		self.width = width
		self.height = height
		self.line_width = round(5 * self.cell_size / Display.JEWEL_SIZE)
		self.selected : list[Jewel] = []
		self.finished = False
		self.locked = False
		self.__initialize_jewels()

	def __repr__(self):
		repr = ""

		for row in self.jewels:
			repr += "[ "
			for jewel in row:
				repr += f"{jewel}, "
			repr += "]\n"

		return repr

	def __initialize_jewels(self, breakable_allowed=False) -> None:
		self.jewels : list[list[Jewel]]= []
		self.jewels_next : list[list[Jewel]]= []

		for row in range(self.height):
			self.jewels.append([])
			self.jewels_next.append([])

			for col in range(self.width):
				type_index = randint(0, len(Game.JEWEL_TYPES) - 1)
				jewel_type = Game.JEWEL_TYPES[type_index]
				jewel = Jewel(0, col, self.cell_size, self.pos, jewel_type)

				Thread(target=jewel.update, args=(row, col, 0.015)).start()

				self.jewels[row].append(jewel)
				self.jewels_next[row].append(jewel)

		if breakable_allowed:
			return

		while True:
			breakable = self.__get_breakable_jewels()
			if len(breakable) < 1:
				break

			for jewel in breakable:
				jewel.respawn()

	def __is_moving(self) -> bool:
		for col in range(len(self.jewels[0])):
			for row in range(len(self.jewels) - 1, 0, -1):
				if self.jewels[row][col].state == JEWEL_MOVING:
					return True

		return False

	def __wait_until_is_idle(self) -> None:
		def wait():
			while self.__is_moving(): 
				sleep(0.01)

		thread = Thread(target=wait)
		thread.start()
		thread.join()
				
	def __pull_down(self) -> None:
		pull_again = False

		self.__wait_until_is_idle()

		# pull down gems checking from bottom to top
		# we don't need to check the last gem (uppermost)
		for col in range(len(self.jewels[0]) - 1, -1, -1):
			for row in range(len(self.jewels) - 1, 0, -1):
				jewel = self.jewels[row][col]
				upper_jewel = self.jewels[row - 1][col]

				if jewel.state == JEWEL_CRUSHED and upper_jewel.state == JEWEL_IDLE:
					#print(f"swapping: {jewel} and {upper_jewel}")
					self.free_swap((jewel, upper_jewel), False, delta=0.002)
					pull_again = True

		if pull_again:
			self.__pull_down()
		else:
			for col in range(len(self.jewels[0])):
				for row in range(len(self.jewels)):
					if self.jewels[row][col].state == JEWEL_MOVING:
						self.jewels[row][col].set_state(JEWEL_IDLE)
				
	def __refill(self):
		self.__wait_until_is_idle()

		for row in range(self.height):
			for col in range(self.width):
				existing_jewel = self.jewels[row][col]
				if existing_jewel.state != JEWEL_CRUSHED:
					continue

				type_index = randint(0, len(Game.JEWEL_TYPES) - 1)
				jewel_type = Game.JEWEL_TYPES[type_index]
				jewel = Jewel(0, col, self.cell_size, self.pos, jewel_type)

				Thread(target=jewel.update, args=[row, col, 0.015]).start()

				self.jewels[row][col] = jewel

	def __are_neighbors(self, jewel: Jewel, other_jewel: Jewel) -> bool:
		if jewel.row == other_jewel.row + 1 and jewel.col == other_jewel.col \
		or jewel.row == other_jewel.row - 1 and jewel.col == other_jewel.col \
		or jewel.row == other_jewel.row and jewel.col == other_jewel.col + 1 \
		or jewel.row == other_jewel.row and jewel.col == other_jewel.col - 1: \
			return True

		return False

	def __get_breakable_jewels(self, check_next_move=False) -> list[Jewel]:
		jewels = self.jewels_next if check_next_move else self.jewels
		breakable : list[Jewel] = []

		for row in jewels:
			last_type = None
			group : list[Jewel] = []

			for jewel in row:
				if jewel.state == JEWEL_CRUSHED:
					continue
				if jewel.type == last_type:
					group.append(jewel)
				else:
					if len(group) >= 3:
						breakable += group

					group = [jewel]

				last_type = jewel.type
			if len(group) >= 3:
				breakable += group

		for col in range(len(jewels[0])):
			last_type = None
			group : list[Jewel] = []

			for row in range(len(jewels)):	
				jewel = jewels[row][col]
				if jewel.type == last_type:
					group.append(jewel)
				else:
					if len(group) >= 3:
						breakable += group

					group = [jewel]

				last_type = jewel.type
			if len(group) >= 3:
				breakable += group

		return breakable

	@lock_board
	def update(self, updates_in_a_row: int = 1):
		while True:
			all_jewels_are_idle = True
			for row in self.jewels:
				for jewel in row:
					if jewel.state == JEWEL_MOVING:
						all_jewels_are_idle = False

			if all_jewels_are_idle:
				break

			sleep(0.01)

		breakable = self.__get_breakable_jewels()
		#print(breakable)
		if len(breakable) < 1:
			return

		threads = [ Thread(target=jewel.crush) for jewel in breakable ]
		choice(Sound.CLICK_SOUNDS).play()
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()

		event = GameEvent(CRUSH_JEWEL_EVENT, [breakable, updates_in_a_row])
		GameEventEmitter.emit(event)
		self.__pull_down()
		self.__refill()

		sleep(0.01)

		self.update(updates_in_a_row + 1)

	def draw(self, surface: Surface) -> None:
		self.draw_brackground(surface, 60, 1)

		x, y = self.pos

		for row in range(len(self.jewels) + 1):
			start = x, row * self.cell_size + y
			end =  self.width * self.cell_size + x, row * self.cell_size + y
			pygame.draw.line(surface, self.color, start, end, self.line_width)

		for col in range(len(self.jewels[0]) + 1):
			start = col * self.cell_size + x, y
			end = col * self.cell_size + x, self.height * self.cell_size + y
			pygame.draw.line(surface, self.color, start, end, self.line_width)

		for row in self.jewels:
			for jewel in row:
				jewel.draw(surface)

	def select(self, pos: tuple[int, int]) -> Jewel | None:
		if self.locked:
			return
		
		x, y = self.pos
		selection_x, selection_y = pos

		if selection_x < x or selection_y < y:
			return None

		if selection_x > self.width * self.cell_size + x or selection_y > self.height * self.cell_size + y:
			return None

		selection_row = int((selection_y - y) / self.cell_size)
		selection_col = int((selection_x - x) / self.cell_size)

		jewel = self.jewels[selection_row][selection_col]
		if jewel.state != JEWEL_IDLE:
			return None

		for selected in self.selected:
			if selected == jewel:
				return None

		self.selected.append(jewel)
		jewel.highlighted = True

		return jewel

	def can_try_swap(self) -> bool:
		return len(self.selected) > 1

	@clear_selected
	def swap(self) -> bool:
		if len(self.selected) != 2:	
			return False

		if self.__are_neighbors(self.selected[0], self.selected[1]):
			self.free_swap((self.selected[0], self.selected[1]))
			event = GameEvent(MOVE_JEWEL_EVENT)
			GameEventEmitter.emit(event)
			return True

		return False

	def free_swap(self, jewels: tuple[Jewel, Jewel], end_movement: bool = True, delta: float = 0.01) -> None:
		temp_row, temp_col = jewels[0].row, jewels[0].col
		temp_jewel = self.jewels[temp_row][temp_col]

		self.jewels[jewels[0].row][jewels[0].col] = self.jewels[jewels[1].row][jewels[1].col]
		self.jewels[jewels[1].row][jewels[1].col] = temp_jewel

		threads = (
			Thread(target=jewels[0].update, args=[jewels[1].row, jewels[1].col, delta]),
			Thread(target=jewels[1].update, args=[temp_row, temp_col, delta])
		)

		for thread in threads:
			thread.start()

	def game_over(self):
		self.finished = True
