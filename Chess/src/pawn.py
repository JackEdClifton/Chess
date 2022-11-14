
from src.board_piece import BoardPiece
from src.vector2 import Vector2

class Pawn(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str, white:bool=True):
		super().__init__(pos, img_path)
		self.is_white = white
		self.is_first_move = True

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
		if self.is_first_move:
			target_pos = self.pos + Vector2(0, y_vel*2)
			if game.get_from_posision(target_pos) == None:
				moves.append(target_pos)

		return moves

	# move the sprite
	def move_to(self, pos):
		self.pos = pos
		self.is_first_move = False