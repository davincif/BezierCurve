from curve import Curve
from point import Point2D
from vector import Vector2D

class Curvature(Curve):

	__prime = [] #prime derivative
	__second = [] #seconde derivative
	__bcurve = [] #hold the bezier curve to calculate the curvature
	smiddle = None #screen middle Point

	def __init__(self, smiddle_x, smiddle_y):
		super()

		self.color = "#ff0000"
		self.show_points = False
		self.show_lines = False
		self.smiddle = Point2D(smiddle_x, smiddle_y)

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
				self._lop[n] = origin + self._lop[n]
				print(self._lop[n])

			#fiting curve on screen
			start_p = self.get_start_drawing_point() #starting point
			if start_p is not None:
				for n in range(0, len(self._lop)):
					self._lop[n] += start_p
			else:
				print("The curvature curve is too big for this window!")
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

	def get_start_drawing_point(self):
		###
		# retuns a point on the screen where the
		# printing of the curve must be start
		# or None if the point is out of the window
		###

		min_p, max_p = self.get_max_min_point() #minimum and maximum point
		print("min_p, max_p", min_p, max_p)
		#since the screen goes right and down as (++) quadrant, min_p is the start draw point

		#the point in the middle of the drawing
		middle_p = (min_p - max_p) #middle point
		middle_p = Point2D(middle_p.x/2, middle_p.y/2)
		middle_p = middle_p + min_p

		#the vector to bring
		start_p = min_p + (self.smiddle - middle_p)

		return Point2D(start_p.x, start_p.y)

	def get_max_min_point(self):
		###
		# retuns 2 points:
		#	 Point2D(max x in lop, max y in lop)
		#	 Point2D(min x in lop, min y in lop)
		###

		max_x = -999999
		max_y = -999999
		min_x = 999999
		min_y = 999999

		for n in range(0, len(self._lop)):
			if self._lop[n].x > max_x:
				max_x = self._lop[n].x
			elif self._lop[n].x < min_x:
				min_x = self._lop[n].x
			
			if self._lop[n].y > max_y:
				max_y = self._lop[n].y
			elif self._lop[n].y < min_y:
				min_y = self._lop[n].y

		return Point2D(max_x, max_y), Point2D(min_x, min_y)
