

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_tuple(self):
		return (self.x, self.y)

	def get_copy(self):
		return Vector2(self.x, self.y)

	# print object
	def __repr__(self):
		return f"({str(self.x)}, {str(self.y)})"

	# math
	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)
	def __mul__(self, other):
		return Vector2(self.x * other.x, self.y * other.y)

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		return False

	def __ne__(self, other):
		return not self.__eq__(other)
