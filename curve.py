from Point import Point2D
import numbers

class Curve:
	lop = [] #list of points

	#OVERWRITE METHODS
	def __init__(self, l):
		if not type(l) is list:
			raise Exception("argument to create a curve must be a list of numbers")

		aux = max(l)
		n = 0
		while n < aux:
			if not isinstance(l[n], numbers.Number) or not isinstance(l[n+1], numbers.Number):
				raise Exception("curve must be only numbers in the list to create a curve")

			self.lop.append(Point2D(l[n], l[n+1]))
			n += 2

	def __str__(self):
		return str(self.printable())


	#COMMON METHODS
	def add_point(self, x, y):
		self.lop += [Point2D(x,y)]

	def printable(self):
		lp = []
		for elem in self.lop:
			lp.append(elem.x)
			lp.append(elem.y)
		return lp

	#AUXILIAR METHODS