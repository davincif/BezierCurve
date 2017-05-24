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
	show_points = True #show the points of the curve
	show_lines = True #show the lines of the curve
	__std_bshow = None #standard Bezier curve show mod (with is, with lines and no points). if curve is bezier, it's a bool
	color = '#000000' #default line color
	delt = 0.5 #the 't' parameter of the derivation -this attribute only make difference when in the master curve

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

	def make_master(self):
		if self.__bezier:
			raise Exception("This curve is already a bezier curve, can't be master as well")
		self.__master = True
		self.__derivative = []

	def make_bezier(self):
		if self.__master:
			raise Exception("This curve is already a master curve, can't be bezier as well")
		self.__bezier = True
		self.__degree = -1
		self.show_points = False
		self.__std_bshow = True
		self.color = "#0000ff"

	def toggle_show(self):
		self.show_lines = not self.show_lines
		self.show_points = not self.show_points

	def toggle_bcurve_show(self):
		if self.__bcurve is not None:
			self.__bcurve.show_lines = not self.__bcurve.show_lines
			if not self.__bcurve.__std_bshow:
				self.__bcurve.show_points = not self.__bcurve.show_points

	def toggle_bcurve_points(self):
		if self.__bcurve is not None:
			if not self.__bcurve.__std_bshow:
				self.__bcurve.show_points = not self.__bcurve.show_points
			else:
				print("cant show bezier points, its a standard curve")

	def toggle_bcurve_lines(self):
		if self.__bcurve is not None:
			self.__bcurve.show_lines = not self.__bcurve.show_lines

	def toggle_bcurve_std(self):
		self.__bcurve.__std_bshow = not self.__bcurve.__std_bshow
		self.__bcurve.show_points = False


	def toggle_derivated_show(self):
		if self.__delc is not None:
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
		r = r + int(255*percentual)
		g = g + int(255*percentual)
		b = b + int(255*percentual)
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
				self.calc_degree()
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
			self.calc_degree()

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

		if self.show_points or self.show_lines:
			n = 0
			while n < self.__lopS:
				if self.show_points:
					#do not draw the bezier curve points
					item = canva.create_oval(self.__lop[n].x - self.psize, self.__lop[n].y - self.psize, self.__lop[n].x + self.psize, self.__lop[n].y + self.psize, fill=self.color)
					if self.__master:
						canva.itemconfig(item, tags="master")
					elif self.__bezier:
						canva.itemconfig(item, tags="bezier")
					else:
						canva.itemconfig(item, tags="derivative"+str(self.__degree))

				if self.show_lines and n != self.__lopS-1:
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

	def calc_degree(self):
		if not self.__bezier:
			self.__degree = self.__lopS - 1

	def calc_derivatives(self):
		if not self.__master:
			raise Exception("only the master cusve can be derivated")
		elif self.__degree < 1:
			print("The curve must have at least degree 1, but has only " + str(self.__degree))
		else:
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
						newc.__add_point((1-self.delt)*prevc.__lop[itr2] + self.delt*prevc.__lop[itr2+1])
					itr2 += 1
				newc.decay_color(0.3, (230, 230, 230))
				itr1 += 1
			newc.change_color((0, 0, 255))

	def calc_bezier(self, intervals):
		if self.__degree > 1:
			#ok calculate it!
			self.__bcurve = Curve()
			self.__bcurve.make_bezier()
			bcaux = self.__bcurve #Bezier curve auxiliar
			bcaux.__lop = []
			step = 1/intervals
			self.delt = 0.0
			while (self.delt - 1.0) < 0.0000001: #self.delt == 1.0 -> float precision problem
				self.calc_derivatives()
				bcaux.__add_point(self.__delc[len(self.__delc)-1].__lop[0])
				self.delt += step
			self.__delc = None
		elif self.__degree == -1:
			print("it already is a bezier curve")
		else:
			print("The curve must have at least degree 2, but has only " + str(self.__degree))
