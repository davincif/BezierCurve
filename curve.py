import numbers
from point import Point2D
from vector import Vector2D
import bt

class Curve:
	#CURVE'S MATH ATTRIBUTES
	__lop = [] #list of points
	__lopS = 0 #lop size
	__degree = 0 #the curve's degree
	__master = False #if the curve is the controll point course
	__bezier = False #if this curve is the last curve, the bezier curve
	__delc = None #the derivated curves. -this parameter is [Curve,...,Curve] if the curve is master
	__bcurve = None #the Bezier curve. -this parameter is a Curve when calculated

	#APPEARANCE ATTRIBUTES
	psize = 3 #the radius of the point size, in pixels
	thickness = 1 #default width of the line
	__shown = True #if the curve is being shown or not
	color = 'black' #default line color

	#OVERWRITE METHODS
	def __init__(self):
		pass

	def __str__(self):
		string = ""

		if self.__master:
			string += "grau " + str(self.__degree)
			string += " master "
		elif self.__bezier:
			string += " bezier "
		else:
			string += "grau " + str(self.__degree) + " "

		string += str(self.printable())
		return string

	#"PROTECTED" ATTRIBUTE MANIPULATE METHODS
	def isMaster(self):
		return self.__master

	def isBezier(self):
		return self.__bezier

	def makeMaster(self):
		if self.__bezier:
			raise Exception("This curve is already a bezier curve, can't be master as well")
		self.__master = True
		self.__derivative = []

	def makeBezier(self):
		if self.__master:
			raise Exception("This curve is already a master curve, can't be bezier as well")
		self.__bezier = True
		self.__degree = -1
		self.color = "blue"

	def isShown(self):
		return self.__shown

	def toggleShow(self):
		self.__shown = not self.__shown

	def show(self, option):
		if type(option) is bool:
			self.__shown = option
		else:
			raise Exception("toogle the show stat you need to pass a bool argument")


	#COMMON METHODS
	def add_point(self, x, y):
		if isinstance(x, numbers.Number) and isinstance(y, numbers.Number):
			self.__lop += [Point2D(x,y)]
			self.__lopS += 1
			if not self.__bezier:
				self.calcDegree()
		else:
			raise Exception("need Curve.add_point(number, number), got (" + str(type(x)) + ", " + str(type(y)) + ")")

	def __add_point(self, point):
		if type(point) is Point2D:
			self.__lop += [point]
		elif type(point) is Vector2D:
			self.__lop += [Point2D(point.x, point.y)] #equivalent to point + Point2D(0, 0)
		else:
			raise Exception("need Curve.__add_point(Point2D), got (" + str(type(point)) + ")")
		self.__lopS += 1
		if not self.__bezier:
			self.calcDegree()

	def printable(self):
		lp = []
		for elem in self.__lop:
			lp.append(elem.x)
			lp.append(elem.y)
		return lp

	def draw(self, canva):
		if self.__shown:
			n = 0
			while n < self.__lopS:
				canva.create_oval(self.__lop[n].x - self.psize, self.__lop[n].y - self.psize, self.__lop[n].x + self.psize, self.__lop[n].y + self.psize, fill=self.color)
				if n != self.__lopS-1:
					canva.create_line(self.__lop[n].x, self.__lop[n].y, self.__lop[n+1].x, self.__lop[n+1].y, width=self.thickness, fill=self.color)
				n += 1

		if self.__delc is not None:
			itr = 0 #iterator
			while itr < self.__degree:
				self.__delc[itr].draw(canva)
				itr += 1

		if self.__bcurve is not None:
			self.__bcurve.draw(canva)

	def calcDegree(self):
		if not self.__bezier:
			self.__degree = self.__lopS - 1

	def calcDerivatives(self):
		if not self.__master:
			raise Exception("only the master cusve can be derivated")
		elif self.__degree < 1:
			print("The curve must have at least degree 1, but has only " + str(self.__degree))
		elif self.__delc is not None and len(self.__delc) > 0:
			print("This curve already was derivated")
		else:
			prevc = self #previous curve
			newc = self #current curve
			self.__delc = []
			itr1 = 0 #iterator 1
			while itr1 < self.__degree:
				self.__delc += [Curve()]
				self.__delc[itr1].__lop = []
				if itr1 == 0:
					prevc = self
					newc = self.__delc[itr1]
				else:
					prevc = self.__delc[itr1-1]
					newc = self.__delc[itr1]
				itr2 = 0 #iterator 2
				while itr2 < prevc.__lopS-1:
					#derivate
					newc.__add_point(0.5*prevc.__lop[itr2] + 0.5*prevc.__lop[itr2+1])
					itr2 += 1
				itr1 += 1
			newc.color = "Blue"

	def calcBezier(self):
		if self.__bcurve is not None:
			print("Bezier curve is already calculated")
		elif self.__degree > 1:
			#ok calculate it!
			self.__bcurve = Curve()
			bcaux = self.__bcurve #Bezier curve auxiliar
			bcaux.__lop = []
			bcaux.makeBezier()
			intervals = 2
			t = 1/intervals

			n = self.__degree
			i = 0
			while i < n:
				# point = self.__lop[i] * (bt.pt[n-1][i] * (1 - t)**(n-i) * t**i)
				# bcaux.__add_point(point + (self.__lop[i] - point))
				bcaux.__add_point(self.__lop[i] * (bt.pt[n-1][i] * (1 - t)**(n-i) * t**i))
				i += 1
			print(bcaux)
		elif self.__degree == -1:
			print("it already is a bezier curve")
		else:
			print("The curve must have at least degree 2, but has only " + str(self.__degree))
