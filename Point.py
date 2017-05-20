class Point2D:
	#x - double position
	#y - double position

	#OVERWRITE METHODS
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return ".(" + str(self.x) + ", " + str(self.y) + ")"

	def __add__(self, other):
		return Point2D(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Point2D(self.x - other.x, self.y - other.y)

	def __neg__(self):
		return Point2D(-self.x, -self.y)

	#COMMON METHODS

	#AUXILIAR METHODS
