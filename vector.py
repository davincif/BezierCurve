import numbers
import math

class Vector2D:
	x = None
	y = None

	#OVERWRITE METHODS
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "-->(" + str(self.x) + ", " + str(self.y) + ")"

	def __add__(self, other):
		if type(other) is Vector2D:
			return Vector2D(self.x + other.x, self.y + other.y)
		else:
			raise Exception("can't add " + str(type(self)) + " with " + str(type(other)) + ".")

	def __sub__(self, other):
		if type(other) is Vector2D:
			return Vector2D(self.x - other.x, self.y - other.y)
		else:
			raise Exception("can't sub " + str(type(self)) + " with " + str(type(other)) + ".")

	def __mul__(self, other):
		if isinstance(other, numbers.Number):
			return Vector2D(other * self.x, other * self.y)
		elif type(other) is Vector2D:
			return Vector2D(self.x * other.x, self.y * other.y)
		else:
			raise Exception("can't sub " + str(type(self)) + " with " + str(type(other)) + ".")

	def __rmul__(self, other):
		return self.__mul__(other)

	def __truediv__(self, other):
		if isinstance(other, numbers.Number):
			return Vector2D(self.x / other, self.y / other)
		else:
			raise Exception("can only divide vector by numbers (in thos order)")

	#COMMON METHODS
	def module(self):
		return math.sqrt(self.x**2 + self.y**2) 
