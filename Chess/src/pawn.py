
from src.board_piece import BoardPiece
from src.vector2 import Vector2

class Pawn(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str):
		super().__init__(pos, img_path)
		self.home_row = pos.y

	def get_moves(self, game) -> list:

		# list for valid moves
		moves = []

		# get direction of movement based on team
		y_vel = -1 if self.is_white else 1

		# check moving up one position
		target_pos = self.pos + Vector2(0, y_vel)
		if game.get_from_posision(target_pos) == None:
			moves.append(target_pos)

		# check moving up 2 positions
		if self.pos.y == self.home_row:
			target_pos = self.pos + Vector2(0, y_vel*2)
			if game.get_from_posision(target_pos) == None:
				moves.append(target_pos)

		# check diagonal moves
		for x_vel in (-1, 1):
			target_pos = self.pos + Vector2(x_vel, y_vel)
			sprite_in_target = game.get_from_posision(target_pos)
			if sprite_in_target == None:
				pass
			elif sprite_in_target.is_white != self.is_white:
					moves.append(target_pos)

		return moves
