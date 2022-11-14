

from src.board_piece import BoardPiece
from src.vector2 import Vector2

class Knight(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str):
		super().__init__(pos, img_path)


	def get_moves(self, game) -> list:

		# list for valid moves
		moves = []

		# iterate through directions (TODO: simplify)
		displacements = [
			(-2, -1),
			(-2, 1),
			(-1, -2),
			(-1, 2),
			(1, -2),
			(1, 2),
			(2, -1),
			(2, 1),
		]

		# check all movements
		for displacement in displacements:
			target_pos = self.pos + Vector2(*displacement)

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

