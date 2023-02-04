
import pygame
from src.vector2 import Vector2

# abstract class for board pieces
class BoardPiece:
	def __init__(self, pos: Vector2, img_path: str):
		self.pos = pos
		self.fallback_pos = pos
		self.surface = pygame.transform.scale(pygame.image.load(img_path), (75, 75))
		self.is_white = bool(img_path.count("white"))

	# check if space is outside board
	def is_space_on_board(self, x, y):
		return x in range(8) and y in range(8)

	# get all the moves in a single direction
	def get_moves_for_direction(self, game, x_multiplier, y_multiplier):

		# list for valid moves
		moves = []

		# check for moves in axis
		for vel in range(1, 8):
			target_pos = self.pos + Vector2(vel*x_multiplier, vel*y_multiplier)

			# check outside board
			if not self.is_space_on_board(target_pos.x, target_pos.y):
				break
			
			# get target sprite
			sprite_in_target = game.get_from_posision(target_pos)
			
			if sprite_in_target == None:
				moves.append(target_pos)
				continue

			# if sprite is on team stop
			if sprite_in_target.is_white == self.is_white:
				break

			# add movement point
			moves.append(target_pos)
			
			# if sprite is on other team stop
			if sprite_in_target.is_white != self.is_white:
				break

		# return moves
		return moves

	# get list of valid moves
	def get_moves(self, game) -> list:
		return []

	# move the sprite
	def move_to(self, pos):
		self.fallback_pos = self.pos
		self.pos = pos

	# undo the move (used to stop check)
	def undo_move(self):
		self.pos = self.fallback_pos