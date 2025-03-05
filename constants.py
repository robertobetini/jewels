import os, pygame

class Sound:
	CLICK_SOUND = pygame.mixer.Sound(os.path.join("assets", "click.mp3"))

class Image:
	JEWEL_IMAGES = [
		pygame.image.load(os.path.join("assets", "gems_6_0.png")),
		pygame.image.load(os.path.join("assets", "gems_1_1.png")),
		pygame.image.load(os.path.join("assets", "gems_0_2.png")),
		pygame.image.load(os.path.join("assets", "gems_4_3.png")),
		pygame.image.load(os.path.join("assets", "gems_2_4.png")),
		pygame.image.load(os.path.join("assets", "gems_5_5.png")),
		pygame.image.load(os.path.join("assets", "gems_3_6.png"))
	]
	JEWEL_ICONS = [
		pygame.image.load(os.path.join("assets", "gems_6_0.png")),
		pygame.image.load(os.path.join("assets", "gems_1_1.png")),
		pygame.image.load(os.path.join("assets", "gems_0_2.png")),
		pygame.image.load(os.path.join("assets", "gems_4_3.png")),
		pygame.image.load(os.path.join("assets", "gems_2_4.png")),
		pygame.image.load(os.path.join("assets", "gems_5_5.png")),
		pygame.image.load(os.path.join("assets", "gems_3_6.png"))
	]

class Colors:
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

class Display:
	JEWEL_SIZE = 60

class Text:
	MOVE_COUNTER_TEXT_SIZE = 32
	PROGRESS_GAUGE_TEXT_SIZE = 18

class Game:
	BASE_JEWEL_SCORE = 10
	STARTING_MOVES = 30
	JEWEL_TYPES = [0, 1, 2 , 3, 4, 5, 6]
