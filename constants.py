import os, pygame

from enum import Enum

class Sound:
	CLICK_SOUNDS = [
		pygame.mixer.Sound(os.path.join("assets", "sound", "jewel_break_1.wav")),
		pygame.mixer.Sound(os.path.join("assets", "sound", "jewel_break_2.wav")),
		pygame.mixer.Sound(os.path.join("assets", "sound", "jewel_break_3.wav")),
		pygame.mixer.Sound(os.path.join("assets", "sound", "jewel_break_4.wav")),
		pygame.mixer.Sound(os.path.join("assets", "sound", "jewel_break_5.wav"))
	]

class Image:
	JEWEL_IMAGES = [
		pygame.image.load(os.path.join("assets", "img", "gems_6_0.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_1_1.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_0_2.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_4_3.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_2_4.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_5_5.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_3_6.png"))
	]
	JEWEL_ICONS = [
		pygame.image.load(os.path.join("assets", "img", "gems_6_0.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_1_1.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_0_2.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_4_3.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_2_4.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_5_5.png")),
		pygame.image.load(os.path.join("assets", "img", "gems_3_6.png"))
	]

class Colors:
	BACKGROUND_COLOR = 120, 130, 115
	JEWEL_COLORS = [
		(236, 40,  19 ),
		(43,  237, 135),
		(29,  7,   236),
		(239, 215, 72 ),
		(255, 57,  221),
		(239, 176, 72 ),
		(125, 237, 18 )
	]
	JEWEL_PROGRESS_GAUGE_COLOR = 220, 220, 220
	JEWEL_HIGHLIGHT_COLOR = 180, 220, 200
	SCORE_TEXT_COLOR = 220, 220, 220
	BORDER_COLOR = 110, 118, 113
	GUI_TEXT_COLOR = 220, 220, 220
	MENU_BACKGROUND_PRIMARY_COLOR = 80, 103, 115
	MENU_BACKGROUND_PRYMARY_COLOR_ALPHA = 80
	MENU_BACKGROUND_SECONDARY_COLOR = 0, 0, 0
	MENU_BACKGROUND_SECONDARY_COLOR_ALPHA = 200

class Display:
	MAX_WINDOW_HEIGHT = 1080
	JEWEL_SIZE = 100
	MARGIN_W = 50
	MARGIN_H = 100

class Text:
	MOVE_COUNTER_TEXT_SIZE = 32
	PROGRESS_GAUGE_TEXT_SIZE = 18
	GUI_TEXT_SIZE = 42

	RESUME_BUTTON_TEXT = "RESUME"
	RESTART_BUTTON_TEXT = "RESTART"
	BACK_TO_TITLE_BUTTON_TEXT = "TITLE"
	NEW_GAME_BUTTON_TEXT = "NEW GAME"
	EXIT_BUTTON_TEXT = "EXIT"

	TITLE_MENU_HEADER = "JEWELS"
	PAUSED_MENU_HEADER = "PAUSED"
	GAME_OVER_MENU_HEADER = "GAME OVER"

class Game:
	BOARD_COLS = 10
	BOARD_ROWS = 10
	BASE_JEWEL_SCORE = 10
	STARTING_MOVES = 20
	JEWEL_TYPES = [0, 1, 2 , 3, 4, 5, 6]
	PROGRESS_MAP = {
		1: 100,
		2: 160,
		3: 250,
		4: 390,
		5: 540
	}

class LogLevel(Enum):
	ERROR = 0
	WARN  = 1
	INFO  = 2
	DEBUG = 3

	def __gt__(self, other):
		return self.value > other.value

	def __lt__(self, other):
		return self.value < other.value

class Log:
	LOG_LEVEL = LogLevel.DEBUG
	LOG_FILE_PATH = "./log.txt"
