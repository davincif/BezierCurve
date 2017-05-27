from curve import Curve
from point import Point2D
from vector import Vector2D

class Curvature(Curve):
	def __init__(self):
		super()
		self.color = "#ff0000"
		#deleting useless attibuts
		self._degree = 3
		del self._degree
		self._master = False
		del self._master
		self._bezier = False
		del self._bezier
		self._delc = []
		del self._delc
		self._bcurve = []
		del self._bcurve

	#COMMON METHODS
	def erase(self):
		self._lop = []
		self.show_points = False
		self.show_lines = False

	def add_points(self, lop):
		if not type(lop) is list:
			errormsg = "argument to create a curve must be a " + str(type(lop)) + " of " + str(type(Point2D))
			if lop is None:
				raise Exception(errormsg)
			elif len(lop) == 0:
				raise Exception(errormsg + "but given was an empty list")
			else:
				raise Exception(errormsg)

		self.show_lines = True
		for elem in lop:
			if not type(elem) is Point2D and not type(elem) is Vector2D:
				raise Exception("there must be only points or vectors in the list to create a curve")
			self._add_point(elem)

	def calc_bcurce_curvature(self, mcurve):
		l = []
		bcurve = mcurve._bcurve
		if bcurve is not None:
			for n in range(0, len(bcurve._lop)-1):
				vec = bcurve._lop[n+1] - bcurve._lop[n]
				l  += [mcurve._lop[0] + ((vec) * 10)]
		else:
				print("There's no bezier curve to calculate its curvature")

		if len(l) == 0:
			return
		else:
			return l

	def draw(self, canva):
		canva.delete("ccurve")
		if self.show_points or self.show_lines:
			for n in range(0, self._lopS):
				if self.show_points:
					item = canva.create_oval(self._lop[n].x - self.psize, self._lop[n].y - self.psize, self._lop[n].x + self.psize, self._lop[n].y + self.psize, fill=self.color)
					canva.itemconfig(item, tags="ccurve")

				if self.show_lines and n != self._lopS-1:
					item = canva.create_line(self._lop[n].x, self._lop[n].y, self._lop[n+1].x, self._lop[n+1].y, width=self.thickness, fill=self.color)
					canva.itemconfig(item, tags="ccurve")
