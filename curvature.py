from curve import Curve
from point import Point2D
from point import Vector2D

class Curvature(Curve):

	__prime = [] #prime derivative
	__second = [] #seconde derivative
	__bcurve = [] #hold the bezier curve to calculate the curvature
	window_size = None #screen dimentions
	is_calced = False # if this curvature was already calculated

	def __init__(self, win_x, win_y):
		super()

		self.color = "#ff0000"
		self.show_points = False
		self.show_lines = False
		self.window_size = Point2D(win_x, win_y)

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
		###
		# x'(t)y''(t) - y'(t)x''(t) 
		# _________________________		curvature
		# (x'(t)² y'(t)²)^(3/2)
		###

		self.is_calced = True

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
				self.__prime += [(self.__bcurve[n+1] - self.__bcurve[n]).make_point()]

			#second derivative
			for n in range(0, len(self.__prime)-1):
				self.__second += [(self.__prime[n+1] - self.__prime[n]).make_point()]

			#curvature
			for n in range(0, len(self.__second)):
				self._lop += [(self.__prime[n].x*self.__second[n].y -  self.__prime[n].y*self.__second[n].x) / (self.__prime[n].module())**3]
				self._lop[n] = Point2D(self.__bcurve[n].x, 1/self._lop[n])

			#fiting curve on screen
			self.resize_curve()
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

	def resize_curve(self):
		###
		# 
		###

		start_p, size = self.get_dimentions()

		x_factor = 1
		y_factor = 1
		stretch_factor = 1

		#calculating resize vector
		# changing coordinate
		# change_coord = start_p/2 - Point2D(0, 0)


		#mensuring factors
		if size.x > self.window_size.x:
			x_factor = self.window_size.x / size.x

		if size.y > self.window_size.y:
			y_factor = self.window_size.y / size.y

		if x_factor != y_factor:
			stretch_factor = min([x_factor, y_factor])

		#calculating translation vector
		translation = Point2D(20, 20) - start_p

		print("translation: ", translation)
		print("stretch_factor: ", stretch_factor)
		#appling transformations
		for n in range(0, len(self._lop)):
			self._lop[n] = self._lop[n]*stretch_factor + translation
			print(self._lop[n])

	def get_dimentions(self):
		###
		# get dimentions
		###

		max_x = self._lop[0].x
		max_y = self._lop[0].y
		min_x = self._lop[0].x
		min_y = self._lop[0].y

		for n in range(1, len(self._lop)):
			if self._lop[n].x > max_x:
				max_x = self._lop[n].x
			elif self._lop[n].x < min_x:
				min_x = self._lop[n].x
			
			if self._lop[n].y > max_y:
				max_y = self._lop[n].y
			elif self._lop[n].y < min_y:
				min_y = self._lop[n].y

		#since the screen goes right and down as (++) quadrant, min_p is the start draw point
		return Point2D(min_x, min_y), Vector2D(max_x - min_x, max_y - min_y)
