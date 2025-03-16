import pygame

from time import sleep
from random import randint
from pygame import Rect, Surface

from constants import Display, Game, Image, Colors
from entities import Entity
from errors import InvalidJewelStateError

JEWEL_SIZE = Display.JEWEL_SIZE

# states
JEWEL_IDLE = 0
JEWEL_MOVING = 1
JEWEL_CRUSHED = 2

class Jewel(Entity):
	JEWEL_STATES = [JEWEL_IDLE, JEWEL_MOVING, JEWEL_CRUSHED]
	JEWEL_STATE_NAMES = {
		JEWEL_IDLE: "JEWEL_IDLE",
		JEWEL_MOVING: "JEWEL_MOVING",
		JEWEL_CRUSHED: "JEWEL_CRUSHED"
	}

	def __init__(self, row: int, col: int, jewel_size: int, offset: tuple[int, int] = (0, 0), type: int = 0):
		self.offset = offset
		offset_x, offset_y = self.offset
		pos = col * jewel_size + offset_x, row * jewel_size + offset_y
		super().__init__(pos, size=(jewel_size, jewel_size))

		self.row = row
		self.col = col
		self.jewel_size = jewel_size
		self.type = type
		self.image = pygame.transform.scale(Image.JEWEL_IMAGES[type], (self.jewel_size, self.jewel_size))
		self.state = JEWEL_IDLE
		self.hidden = False
		self.angle = 0
		self.highlighted = False
		self.highlight_color = Colors.JEWEL_HIGHLIGHT_COLOR
		self.line_width = round(5 * jewel_size / Display.JEWEL_SIZE)

	def __repr__(self) -> str:
		return f"<{self.type}>[{self.row}, {self.col}] = {Jewel.JEWEL_STATE_NAMES[self.state]}"

	def __str__(self) -> str:
		return self.__repr__()

	def __eq__(self, other) -> bool:
		if other == None:
			return False

		return self.row == other.row and self.col == other.col and self.type == other.type

	def __update_image(self):
		self.image = pygame.transform.scale(Image.JEWEL_IMAGES[self.type], (self.jewel_size, self.jewel_size))

	def set_state(self, state: int):
		if state not in Jewel.JEWEL_STATES:
			raise InvalidJewelStateError(state)

		self.state = state

	def draw(self, surface: Surface) -> None:
		if not self.hidden:
			self.image = pygame.transform.rotate(self.image, self.angle)
			surface.blit(self.image, self.pos)
			if self.highlighted:
				rect = Rect(self.pos, self.size)
				pygame.draw.rect(surface, self.highlight_color, rect, self.line_width)

	def update(self, row: int, col: int, delta: float = 0.01, end_movement = True) -> None:
		offset_x, offset_y = self.offset
		new_pos = col * self.jewel_size + offset_x, row * self.jewel_size + offset_y
		
		self.row = row
		self.col = col

		current_x, current_y = self.pos
		new_x, new_y = new_pos

		updates = 40
		if self.state != JEWEL_CRUSHED:
			self.set_state(JEWEL_MOVING)

		for i in range(updates - 1):
			amount_x, amount_y = (new_x - current_x) // 5, (new_y - current_y) // 5
			if abs(amount_x) < 1 and abs(amount_y) < 1:
				break

			current_x, current_y = self.pos
			self.pos = current_x + amount_x, current_y + amount_y
			sleep(delta)

		self.pos = new_pos
		if end_movement and self.state != JEWEL_CRUSHED:
			self.set_state(JEWEL_IDLE)

	def crush(self):
		if self.state == JEWEL_CRUSHED:
			return

		while self.state == JEWEL_MOVING:
			sleep(0.01)

		self.set_state(JEWEL_CRUSHED)
		for i in range(10):
			self.angle = i / 6
			self.image.set_alpha(255 - i*26)
			colour = (
				int(255 / (i/2+1)),
				int(255 / (i/2+1)),
				int(255 / (i/2+1)), 
				255
			)
			self.image.fill(colour, special_flags=pygame.BLEND_RGBA_MIN)
			sleep(0.05)
			
		self.hidden = True
		self.highlighted = False

	def respawn(self):
		random_index = randint(0, len(Game.JEWEL_TYPES)) - 1

		self.angle = 0
		self.type = Game.JEWEL_TYPES[random_index]
		self.set_state(JEWEL_IDLE)
		self.__update_image()
		self.hidden = False
		self.highlighted = False
