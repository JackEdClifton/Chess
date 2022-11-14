
import pygame
from src.vector2 import Vector2

# abstract class for board pieces
class BoardPiece:
	def __init__(self, pos: Vector2, img_path: str):
		self.pos = pos
		self.surface = pygame.transform.scale(pygame.image.load(img_path), (75, 75))

	def is_space_free(self, target_pos: Vector2, white_players, black_players) -> bool:
		for sprites in (white_players, black_players):
			for sprite in sprites:
				if target_pos == sprite.pos:
					return False
		return True

	def get_moves(self, game):
		return []

	def move_to(self, pos):
		return