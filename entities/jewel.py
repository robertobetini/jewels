import os, pygame
from sys import flags

from time import sleep
from random import randint
from pygame import Rect, Surface

from constants import JEWEL_IMAGES
from entities.entity import Entity

jewel_images = [
	pygame.image.load(os.path.join("assets", "gems_6_0.png")),
	pygame.image.load(os.path.join("assets", "gems_1_1.png")),
	pygame.image.load(os.path.join("assets", "gems_0_2.png")),
	pygame.image.load(os.path.join("assets", "gems_4_3.png")),
	pygame.image.load(os.path.join("assets", "gems_2_4.png")),
	pygame.image.load(os.path.join("assets", "gems_5_5.png")),
	pygame.image.load(os.path.join("assets", "gems_3_6.png"))
]

# states
JEWEL_IDLE = 0
JEWEL_MOVING = 1
JEWEL_CRUSHED = 2

class Jewel(Entity):
	JEWEL_SIZE = 100
	JEWEL_TYPES = [0, 1, 2 , 3, 4, 5, 6]
	JEWEL_STATES = [JEWEL_IDLE, JEWEL_MOVING, JEWEL_CRUSHED]

	def __init__(self, row: int, col: int, offset: tuple[int, int] = (0, 0), type: int = 0):
		self.offset = offset
		offset_x, offset_y = self.offset
		pos = col * Jewel.JEWEL_SIZE + offset_x, row * Jewel.JEWEL_SIZE + offset_y
		super().__init__(pos, size=(Jewel.JEWEL_SIZE, Jewel.JEWEL_SIZE))

		self.row = row
		self.col = col
		self.type = type
		self.image = pygame.transform.scale(JEWEL_IMAGES[type], (Jewel.JEWEL_SIZE, Jewel.JEWEL_SIZE))
		self.state = JEWEL_IDLE
		self.hidden = False
		self.angle = 0

	def __repr__(self) -> str:
		return f"<{self.type}>[{self.row}, {self.col}] = {self.state}"

	def __str__(self) -> str:
		return self.__repr__()

	def __eq__(self, other) -> bool:
		if other == None:
			return False

		return self.row == other.row and self.col == other.col and self.type == other.type

	def __update_image(self):
		self.image = pygame.transform.scale(jewel_images[self.type], (Jewel.JEWEL_SIZE, Jewel.JEWEL_SIZE))

	def set_state(self, state: int):
		if state not in Jewel.JEWEL_STATES:
			raise Exception(f"Invalid jewel state: {state}")

		self.state = state

	def draw(self, surface: Surface) -> None:
		if not self.hidden:
			self.image = pygame.transform.rotate(self.image, self.angle)
			surface.blit(self.image, self.pos)

	def update(self, row: int, col: int, delta: float = 0.01, end_movement = True) -> None:
		offset_x, offset_y = self.offset
		new_pos = col * Jewel.JEWEL_SIZE + offset_x, row * Jewel.JEWEL_SIZE + offset_y
		
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
			self.angle = i / 5
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

	def respawn(self):
		random_index = randint(0, len(Jewel.JEWEL_TYPES)) - 1

		self.angle = 0
		self.type = Jewel.JEWEL_TYPES[random_index]
		self.set_state(JEWEL_IDLE)
		self.__update_image()
		self.hidden = False
