from curve import Curve
from point import Point2D
from vector import Vector2D

class Curvature(Curve):

	__prime = [] #prime derivative
	__second = [] #seconde derivative
	__bcurve = [] #hold the bezier curve to calculate the curvature

	def __init__(self):
		super()

		self.color = "#ff0000"
		self.show_points = False
		self.show_lines = False

		#deleting useless attibuts
		self._degree = 3
		del self._degree
		self._master = False
		del self._master
		self._delc = []
		del self._delc
		self._bcurve = []
		del self._bcurve

	#COMMON METHODS
	def calc_bcurce_curvature(self, mcurve):
		# x'(t)y''(t) - y'(t)x''(t) 
		# _________________________		curvature
		# (x'(t)² y'(t)²)^(3/2)

		#erase possible old content
		self._lop = []
		self.__prime = []
		self.__second = []
		self.__bcurve = []

		#update bcurve
		self.__bcurve = mcurve._bcurve._lop

		#derivatives
		if self.__bcurve is not None:
			#prime derivative
			for n in range(0, len(self.__bcurve)-1):
				self.__prime += [self.__bcurve[n+1] - self.__bcurve[n]]

			#second derivative
			for n in range(0, len(self.__prime)-1):
				self.__second += [self.__prime[n+1] - self.__prime[n]]

			#curvature
			origin = Point2D(0, 0)
			for n in range(0, len(self.__second)):
				self._lop += [(self.__prime[n].x*self.__second[n].y -  self.__prime[n].y*self.__second[n].x) / (self.__prime[n].x**2 * self.__prime[n].y**2)**(3/2)]
				print(self._lop[n])
				self._lop[n] = origin + self._lop[n]
			print("\n\n")
			for n in range(0, len(self.__second)):
				print(self._lop[n])
		else:
				print("There's no bezier curve to calculate its curvature")

	def draw(self, canva):
		canva.delete("ccurve")

		if self.show_points or self.show_lines:
			for n in range(0, len(self._lop)-1):
				#draw the curve points
				if self.show_points:
					item = canva.create_oval(self._lop[n].x - self.psize, self._lop[n].y - self.psize, self._lop[n].x + self.psize, self._lop[n].y + self.psize, fill=self.color)
					canva.itemconfig(item, tags="ccurve")

				#draw the curve lines
				if self.show_lines:
					item = canva.create_line(self._lop[n].x, self._lop[n].y, self._lop[n+1].x, self._lop[n+1].y, width=self.thickness, fill=self.color)
					canva.itemconfig(item, tags="ccurve")
