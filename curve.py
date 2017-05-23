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
	color = '#000000' #default line color

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
			string += "grau " + str(self.__degree)
			string += " delc "

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
		self.color = "#0000ff"

	def is_shown(self):
		return self.__shown

	def toggle_show(self):
		self.__shown = not self.__shown

	def show(self, option):
		if type(option) is bool:
			self.__shown = option
		else:
			raise Exception("toogle the show stat you need to pass a bool argument")

	def toggle_derivated_show(self):
		for elem in self.__delc:
			elem.toggle_show()

	def change_color(self, rpg):
		self.color = '#%02x%02x%02x' % rpg
		# r, g , b = rgb
		# hex(r) + hex(g)[2:] + hex(b)[2:]

	def decay_color(self, percentual, rgblimit):
		h = "0x" + self.color[1:len(self.color)]
		h1, h2, h3 = h[0:4], '0x' + h[4:6], '0x' + h[6:8]
		r, g , b = int(h1, 16), int(h2, 16), int(h3, 16)
		r = r + (255*percentual)
		g = g + (255*percentual)
		b = b + (255*percentual)
		if r > rgblimit[0]:
			r = rgblimit[0]
		if g > rgblimit[1]:
			g = rgblimit[1]
		if b > rgblimit[2]:
			b = rgblimit[2]
		self.change_color((r,g,b))


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
		if self.__master:
			canva.delete("master")
		elif self.__bezier:
			canva.delete("bezier")
		else:
			canva.delete("derivative"+str(self.__degree))

		if self.__shown:
			n = 0
			while n < self.__lopS:
				item = canva.create_oval(self.__lop[n].x - self.psize, self.__lop[n].y - self.psize, self.__lop[n].x + self.psize, self.__lop[n].y + self.psize, fill=self.color)
				if self.__master:
					canva.itemconfig(item, tags="master")
				elif self.__bezier:
					canva.itemconfig(item, tags="bezier")
				else:
					canva.itemconfig(item, tags="derivative"+str(self.__degree))
				if n != self.__lopS-1:
					item = canva.create_line(self.__lop[n].x, self.__lop[n].y, self.__lop[n+1].x, self.__lop[n+1].y, width=self.thickness, fill=self.color)
					if self.__master:
						canva.itemconfig(item, tags="master")
					elif self.__bezier:
						canva.itemconfig(item, tags="bezier")
					else:
						canva.itemconfig(item, tags="derivative"+str(self.__degree))
				n += 1

		if self.__delc is not None:
			for elem in self.__delc:
				elem.draw(canva)

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
		elif self.__delc is not None and len(self.__delc) == self.__degree:
			print("This curve already was derivated")
		else:
			if self.__delc == None:
				self.__delc = []
			prevc = self #previous curve
			newc = self #current curve
			itr1 = 0 #iterator 1
			while itr1 < self.__degree:
				if itr1 >= len(self.__delc):
					self.__delc += [Curve()]
					self.__delc[itr1].__lop = []

				self.__delc[itr1].color = self.color
				if itr1 == 0:
					prevc = self
					newc = self.__delc[itr1]
				else:
					prevc = self.__delc[itr1-1]
					newc = self.__delc[itr1]

				itr2 = 0 #iterator 2
				while itr2 < prevc.__lopS-1:
					#derivate
					if itr2 >= newc.__lopS:
						newc.__add_point(0.5*prevc.__lop[itr2] + 0.5*prevc.__lop[itr2+1])
					itr2 += 1
				newc.decay_color(0.3, (230, 230, 230))
				itr1 += 1
			newc.change_color((0, 0, 255))

	def calcBezier(self):
		if self.__degree > 1:
			if self.__bcurve is not None:
				del self.__bcurve #so we must recalc it
			#ok calculate it!
			self.__bcurve = Curve()
			self.__bcurve.makeBezier()
			bcaux = self.__bcurve #Bezier curve auxiliar
			bcaux.__lop = []
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
