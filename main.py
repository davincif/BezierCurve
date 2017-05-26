#Bezier curve interactive vizualizer

from curve import Curve
import tkinter as tk
import functools

#GLOBAL VARIABLES
global tolerance
tolerance = 5
global movingPoint
movingPoint = None


#FUNCTIONS
def onclick(event, curve, canva):
	global movingPoint

	movingPoint = curve.is_over_point(event.x, event.y)
	# print("clicekd ", event.x, event.y, "point ", movingPoint)
	if movingPoint is None:
		# print("add point")
		curve.add_point(event.x, event.y)
		curve.draw(canva)

def onmove(event, curve, canva):
	global movingPoint

	if movingPoint is not None:
		movingPoint.x = event.x
		movingPoint.y = event.y
		point, lines = curve.is_showing_bcurve()
		if point or lines:
			curve.calc_bezier(20)
		curve.draw(canva)

def stopMoving(event):
	global movingPoint

	movingPoint = None

def keypress(event, curve, canva):
	#all this is temporary
	if event.char == 'b':
		curve.calc_bezier(20)
		curve.draw(canva)
	elif event.char == 'v':
		curve.toggle_bcurve_show()
		curve.draw(canva)
	elif event.char == 'd':
		curve.delt = 0.5
		curve.calc_derivatives()
		curve.draw(canva)
	elif event.char == 's':
		curve.toggle_derivated_show()
		curve.draw(canva)
	elif event.char == 'q':
		curve.toggle_derivated_show()
		curve.draw(canva)
	else:
		pass


#MAIN
def main():
	mcurve = Curve() #main curve
	mcurve.make_master()
	tolerance = mcurve.psize

	#CREATING CANVA
	tkroot = tk.Tk()
	scrw = tkroot.winfo_screenwidth() #screen width
	scrh = tkroot.winfo_screenheight() #screen height
	print("resolution " + str(scrw) + "x" + str(scrh))
	frame = tk.Canvas(tkroot, width=400, height=400)
	# frame = tk.Canvas(tkroot, width=scrw, height=scrh)
	# tkroot.attributes("-fullscreen", True)
	tkroot.bind('<Button-1>', lambda event: onclick(event, curve=mcurve, canva=frame))
	tkroot.bind("<Key>", lambda event: keypress(event, curve=mcurve, canva=frame))
	tkroot.bind("<B1-Motion>", lambda event: onmove(event, curve=mcurve, canva=frame))
	tkroot.bind("<ButtonRelease-1>", stopMoving)
	frame.pack()
	tk.mainloop()

if __name__ == '__main__':
	main()
