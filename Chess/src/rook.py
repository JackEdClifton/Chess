
from src.board_piece import BoardPiece
from src.vector2 import Vector2

class Rook(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str):
		super().__init__(pos, img_path)


	def get_moves(self, game) -> list:

		# list for valid moves
		moves = []

		# iterate through directions
		moves += self.get_moves_for_direction(game, 0, 1)
		moves += self.get_moves_for_direction(game, 0, -1)
		moves += self.get_moves_for_direction(game, 1, 0)
		moves += self.get_moves_for_direction(game, -1, 0)

		return moves