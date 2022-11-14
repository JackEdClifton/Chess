

from src.board_piece import BoardPiece
from src.vector2 import Vector2

class King(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str):
		super().__init__(pos, img_path)


	def get_moves(self, game) -> list:

		# list for valid moves
		moves = []

		# iterate through directions
		for y in (-1, 0, 1):
			for x in (-1, 0, 1):

				# ignore if no movement is made
				if x == 0 and y == 0:
					continue

				# get target position
				target_pos = self.pos + Vector2(x, y)

				# check space is valid
				if not self.is_space_on_board(target_pos.x, target_pos.y):
					continue

				# get target sprite
				sprite_in_target = game.get_from_posision(target_pos)
			
				# check if space is empty
				if sprite_in_target == None:
					moves.append(target_pos)
					continue

				# if sprite is on team stop
				if sprite_in_target.is_white == self.is_white:
					continue

				# add movement point
				moves.append(target_pos)

		return moves

