from Point import Point2D
import numbers

class Curve:
	lop = [] #list of points
	lopS = 0 #lop size
	dotS = 6 #the dot's size that marks the end of the segments, in pixels

	#OVERWRITE METHODS
	def __init__(self, l):
		if not type(l) is list:
			raise Exception("argument to create a curve must be a list of numbers")

		self.lopS = len(l)
		if self.lopS % 2 != 0:
			raise Exception("there must be a pair amount of numbers to create a curve")
		n = 0
		while n < self.lopS:
			if not isinstance(l[n], numbers.Number) or not isinstance(l[n+1], numbers.Number):
				raise Exception("curve must be only numbers in the list to create a curve")

			self.lop.append(Point2D(l[n], l[n+1]))
			n += 2
		self.lopS /= 2

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

	def draw(self, canva):
		n = 0
		dts2 = self.dotS/2
		while n < self.lopS:
			print(n, self.lopS)
			canva.create_oval(self.lop[n].x - dts2, self.lop[n].y - dts2, self.lop[n].x + dts2, self.lop[n].y + dts2, fill="black")
			if n != self.lopS-1:
				canva.create_line(self.lop[n].x, self.lop[n].y, self.lop[n+1].x, self.lop[n+1].y)
			n += 1

	#AUXILIAR METHODS