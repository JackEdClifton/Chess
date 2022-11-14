

from src.board_piece import BoardPiece
from src.vector2 import Vector2

class Queen(BoardPiece):
	def __init__(self, pos: Vector2, img_path: str):
		super().__init__(pos, img_path)


	def get_moves(self, game) -> list:

		# list for valid moves
		moves = []

		# iterate through directions
		for y in (-1, 0, 1):
			for x in (-1, 0, 1):
				moves += self.get_moves_for_direction(game, x, y)

		return moves
