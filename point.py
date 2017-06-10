import math
import numbers

class Point2D:
	# x = None
	# y = None

	#OVERWRITE METHODS
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return ".(" + str(self.x) + ", " + str(self.y) + ")"

	def __add__(self, other):
		if type(other) is Point2D:
			return Vector2D(self.x + other.x, self.y + other.y)
		elif type(other) is Vector2D:
			return Point2D(self.x + other.x, self.y + other.y)
		elif isinstance(other, numbers.Number):
			return Point2D(self.x + other, self.y + other)
		else:
			raise Exception("can't add " + str(type(self)) + "with" + str(type(other)) + ".")

	def __radd__(self, other):
		return self.__add__(other)

	def __mul__(self, other):
		if isinstance(other, numbers.Number):
			return Point2D(other * self.x, other * self.y)
		elif type(other) is Point2D:
			return Vector2D(self.x * other.x, self.y * other.y)
		else:
			raise Exception("can't multiply " + str(type(self)) + "with" + str(type(other)) + ".")

	def __rmul__(self, other):
		return self.__mul__(other)

	def __sub__(self, other):
		if type(other) is Point2D:
			return Vector2D(self.x - other.x, self.y - other.y)
		elif type(other) is Vector2D:
			return Point2D(self.x - other.x, self.y - other.y)
		elif isinstance(other, numbers.Number):
			return Point2D(self.x - other, self.y - other)
		else:
			raise Exception("can't sub " + str(type(self)) + "with" + str(type(other)) + ".")

	def __rsub__(self, other):
		return self.__add__(other)

	def __neg__(self):
		return Point2D(-self.x, -self.y)

	def __truediv__(self, other):
		if isinstance(other, numbers.Number):
			return Point2D(self.x / other, self.y / other)
		else:
			raise Exception("can only divide point by numbers")

	def __rtruediv__(self, other):
		return self.__truediv__(other)


	#COMMON METHODS
	def make_vector(self):
		return Vector2D(self.x, self.y)

	def r0(self):
		return Vector2D(self.x, self.y)

	def module(self):
		return math.sqrt(self.x**2 + self.y**2)



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
			return Point2D(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		if type(other) is Vector2D:
			return Vector2D(self.x - other.x, self.y - other.y)
		else:
			return Point2D(self.x - other.x, self.y - other.y)
			# raise Exception("can't sub " + str(type(self)) + " with " + str(type(other)) + ".")

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
			raise Exception("can only divide vector by numbers")

	def __rtruediv__(self, other):
		return self.__truediv__(other)

	#COMMON METHODS
	def module(self):
		return math.sqrt(self.x**2 + self.y**2)

	def make_point(self):
		return Point2D(self.x, self.y)
