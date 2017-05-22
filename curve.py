from point import Point2D
import bt

class Curve:
	#CURVE'S MATH ATTRIBUTES
	__lop = [] #list of points
	__lopS = 0 #lop size
	__dotS = 6 #the dot's size that marks the end of the segments, in pixels
	__degree = 0 #the curve's degree
	__master = False #if the curve is the controll point course
	__bezier = False #if this curve is the last curve, the bezier curve
	__derivative = None #the derivated curves. -this parameter is [] if the curve is master

	#APPEARANCE ATTRIBUTES
	thickness = 1 #default width of the line
	__shown = True #if the curve is being shown or not
	color = 'black' #default line color

	#OVERWRITE METHODS
	def __init__(self):
		pass

	def __str__(self):
		if self.__master:
			string = str(self.__degree) + "º"
			string += " master "
		if self.__bezier:
			string += " bezier "
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
		self.__lop += [Point2D(x,y)]
		self.__lopS += 1
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
			dts2 = self.__dotS/2
			while n < self.__lopS:
				canva.create_oval(self.__lop[n].x - dts2, self.__lop[n].y - dts2, self.__lop[n].x + dts2, self.__lop[n].y + dts2, fill=self.color)
				if n != self.__lopS-1:
					canva.create_line(self.__lop[n].x, self.__lop[n].y, self.__lop[n+1].x, self.__lop[n+1].y, width=self.thickness, fill=self.color)
				n += 1

	def calcDegree(self):
		if not self.__bezier:
			self.__degree = self.__lopS - 1

	def calcBezier(self):
		if self.__degree > 2:
			#calculate the derivaive
			t = 0.5 #AINDA NÃO SEI O QUE VOU FAZER COM ESSE PARÂMETRO
			# l[0].x*(1-self.t)
		elif self.__degree == -1:
			print("it already is a bezier curve")
		else:
			print("The curve must have at least degree 3, but has only " + str(self.__degree))
