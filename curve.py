import numbers
from point import Point2D
from vector import Vector2D
import bt

class Curve:
	#CURVE'S MATH ATTRIBUTES
	_lop = [] #list of points
	_lopS = 0 #lop size
	_degree = 0 #the curve's degree
	_master = False #if the curve is the controll point course
	_bezier = False #if this curve is the last curve, the bezier curve
	_delc = None #the derivated curves. -this parameter is [Curve,...,Curve] if the curve is master
	_bcurve = None #the Bezier curve. -this parameter is a Curve when calculated

	#APPEARANCE ATTRIBUTES
	psize = 5 #the radius of the point size, in pixels
	thickness = 1 #default width of the line
	show_points = True #show the points of the curve
	show_lines = True #show the lines of the curve
	_std_bshow = None #standard Bezier curve show mod (with is, with lines and no points). if curve is bezier, it's a bool
	color = '#000000' #default line color
	delt = 0.5 #the 't' parameter of the derivation -this attribute only make difference when in the master curve

	#OVERWRITE METHODS
	def __init__(self):
		pass

	def __str__(self):
		string = ""

		if self._master:
			string += "grau " + str(self._degree)
			string += " master "
		elif self._bezier:
			string += " bezier "
		else:
			string += "grau " + str(self._degree)
			string += " delc "

		string += str(self.printable())
		return string

	#"PROTECTED" ATTRIBUTE MANIPULATE METHODS
	def is_master(self):
		return self._master

	def is_bezier(self):
		return self._bezier

	def make_master(self):
		if self._bezier:
			raise Exception("This curve is already a bezier curve, can't be master as well")
		self._master = True
		self.__derivative = []

	def make_bezier(self):
		if self._master:
			raise Exception("This curve is already a master curve, can't be bezier as well")
		self._bezier = True
		self._degree = -1
		self.show_points = False
		self._std_bshow = True
		self.color = "#0000ff"

	def toggle_show(self):
		self.show_lines = not self.show_lines
		self.show_points = not self.show_points

	def toggle_bcurve_show(self):
		if self._bcurve is not None:
			self._bcurve.show_lines = not self._bcurve.show_lines
			if not self._bcurve._std_bshow:
				self._bcurve.show_points = not self._bcurve.show_points

	def toggle_bcurve_points(self):
		if self._bcurve is not None:
			if not self._bcurve._std_bshow:
				self._bcurve.show_points = not self._bcurve.show_points
			else:
				print("cant show bezier points, its a standard curve")

	def toggle_bcurve_lines(self):
		if self._bcurve is not None:
			self._bcurve.show_lines = not self._bcurve.show_lines

	def toggle_bcurve_std(self):
		self._bcurve._std_bshow = not self._bcurve._std_bshow
		self._bcurve.show_points = False


	def toggle_derivated_show(self):
		if self._delc is not None:
			for elem in self._delc:
				elem.toggle_show()

	def is_showing_derivatives(self):
		if self._delc is not None:
			return self._delc[0].show_points, self._delc[0].show_lines
		return False, False

	def is_showing_bcurve(self):
		if self._bcurve is not None:
			return self._bcurve.show_points, self._bcurve.show_lines
		return False, False

	def derivatives_show(self, sp, sl): #sp = show_points | sl = show_lines
		if self._delc is not None:
			for elem in self._delc:
				elem.show_points = sp
				elem.show_lines = sl

	def bcurve_show(self, sp, sl): #sp = show_points | sl = show_lines
		if self._bcurve is not None:
			self._bcurve.show_lines = sl
			if self._bcurve._std_bshow:
				self._bcurve.show_points = False
			else:
				self._bcurve.show_points = sp



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
			self._lop += [Point2D(x,y)]
			self._lopS += 1
			if not self._bezier:
				self.calc_degree()
		else:
			raise Exception("need Curve.add_point(number, number), got (" + str(type(x)) + ", " + str(type(y)) + ")")

	def _add_point(self, point):
		if type(point) is Point2D:
			self._lop += [point]
		elif type(point) is Vector2D:
			self._lop += [Point2D(point.x, point.y)] #equivalent to point + Point2D(0, 0)
		else:
			raise Exception("need Curve._add_point(Point2D), got (" + str(type(point)) + ")")
		self._lopS += 1
		if not self._bezier:
			self.calc_degree()

	def delete_point(self, point):
		if type(point) is not Point2D:
			raise Exception("this function receives a " + str(type(Point2D)) + ", but given was " + str(type(point)))
		self._lop.remove(point)
		self._lopS -= 1
		if not self._bezier:
			self.calc_degree()

	def printable(self):
		lp = []
		for elem in self._lop:
			lp.append(elem.x)
			lp.append(elem.y)
		return lp

	def draw(self, canva):
		if self._master:
			canva.delete("master")
		elif self._bezier:
			canva.delete("bezier")
		else:
			canva.delete("derivative"+str(self._degree))

		if self.show_points or self.show_lines:
			n = 0
			while n < self._lopS:
				if self.show_points:
					#do not draw the bezier curve points
					item = canva.create_oval(self._lop[n].x - self.psize, self._lop[n].y - self.psize, self._lop[n].x + self.psize, self._lop[n].y + self.psize, fill=self.color)
					if self._master:
						canva.itemconfig(item, tags="master")
					elif self._bezier:
						canva.itemconfig(item, tags="bezier")
					else:
						canva.itemconfig(item, tags="derivative"+str(self._degree))

				if self.show_lines and n != self._lopS-1:
					item = canva.create_line(self._lop[n].x, self._lop[n].y, self._lop[n+1].x, self._lop[n+1].y, width=self.thickness, fill=self.color)
					if self._master:
						canva.itemconfig(item, tags="master")
					elif self._bezier:
						canva.itemconfig(item, tags="bezier")
					else:
						canva.itemconfig(item, tags="derivative"+str(self._degree))
				n += 1

		if self._delc is not None:
			for elem in self._delc:
				elem.draw(canva)

		if self._bcurve is not None:
			self._bcurve.draw(canva)

	def calc_degree(self):
		if not self._bezier:
			self._degree = self._lopS - 1

	def calc_derivatives(self):
		if not self._master:
			raise Exception("only the master cusve can be derivated")
		elif self._degree < 1:
			print("The curve must have at least degree 1, but has only " + str(self._degree))
		else:
			self._delc = []
			prevc = self #previous curve
			newc = self #current curve
			itr1 = 0 #iterator 1
			while itr1 < self._degree:
				if itr1 >= len(self._delc):
					self._delc += [Curve()]
					self._delc[itr1]._lop = []

				self._delc[itr1].color = self.color
				if itr1 == 0:
					prevc = self
					newc = self._delc[itr1]
				else:
					prevc = self._delc[itr1-1]
					newc = self._delc[itr1]

				itr2 = 0 #iterator 2
				while itr2 < prevc._lopS-1:
					#derivate
					if itr2 >= newc._lopS:
						newc._add_point((1-self.delt)*prevc._lop[itr2] + self.delt*prevc._lop[itr2+1])
					itr2 += 1
				newc.decay_color(0.3, (230, 230, 230))
				itr1 += 1
			newc.change_color((0, 0, 255))

	def calc_bezier(self, intervals):
		if self._degree > 1:
			#ok calculate it!
			self._bcurve = Curve()
			self._bcurve.make_bezier()
			bcaux = self._bcurve #Bezier curve auxiliar
			bcaux._lop = []
			step = 1/intervals
			self.delt = 0.0
			while (self.delt - 1.0) < 0.0000001: #self.delt == 1.0 -> float precision problem
				self.calc_derivatives()
				bcaux._add_point(self._delc[len(self._delc)-1]._lop[0])
				self.delt += step
			self._delc = None
		elif self._degree == -1:
			print("it already is a bezier curve")
		else:
			print("The curve must have at least degree 2, but has only " + str(self._degree))

	def is_over_point(self, x, y):
		for elem in self._lop:
			if elem.x - self.psize < x and elem.x + self.psize > x and elem.y - self.psize < y and elem.y + self.psize > y:
				return elem
		return None
