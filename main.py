#Bezier curve interactive vizualizer

from curve import Curve
from curvature import Curvature
import tkinter as tk
import functools

#GLOBAL VARIABLES
global bsegments #segments to construct the bezier curve
bsegments = 35

global movingPoint
movingPoint = None

global mcurve
mcurve = Curve() #main curve
mcurve.make_master()

global curvature #curvature of the bezier curve




#FUNCTIONS
def onclick(event, canva):
	global movingPoint

	movingPoint = mcurve.is_over_point(event.x, event.y)
	if movingPoint is None:
		dpoint, dlines = mcurve.is_showing_derivatives()
		bpoint, blines = mcurve.is_showing_bcurve()

		mcurve.add_point(event.x, event.y)

		if bpoint or blines:
			mcurve.calc_bezier(bsegments)
			mcurve.bcurve_show(bpoint, blines)
		if dpoint or dlines:
			mcurve.delt = 0.5
			mcurve.calc_derivatives()

		if curvature.is_calced:
			curvature.calc_bcurce_curvature(mcurve)

		mcurve.derivatives_show(dpoint, dlines)
		draw(canva)

def onmove(event, canva):
	global movingPoint

	if movingPoint is not None:
		movingPoint.x = event.x
		movingPoint.y = event.y
		dpoint, dlines = mcurve.is_showing_derivatives()
		bpoint, blines = mcurve.is_showing_bcurve()

		if bpoint or blines:
			mcurve.calc_bezier(bsegments)
		if dpoint or dlines:
			mcurve.delt = 0.5
			mcurve.calc_derivatives()

		if curvature.is_calced:
			curvature.calc_bcurce_curvature(mcurve)

		mcurve.bcurve_show(bpoint, blines)
		mcurve.derivatives_show(dpoint, dlines)
		draw(canva)


def stopMoving(event):
	global movingPoint

	movingPoint = None

def toggle_control_lines(event, canva):
	if mcurve.show_lines:
		mcurve.show_lines = False
	elif mcurve.show_points:
		mcurve.show_points = False
	else:
		mcurve.show_lines = True
		mcurve.show_points = True
	draw(canva)

def delete(event, canva):
	mp = mcurve.is_over_point(event.x, event.y) #local moving point
	if mp is not None:
		mcurve.delete_point(mp)

		dpoint, dlines = mcurve.is_showing_derivatives()
		bpoint, blines = mcurve.is_showing_bcurve()
		if bpoint or blines:
			mcurve.calc_bezier(bsegments)
			mcurve.bcurve_show(bpoint, blines)
		if dpoint or dlines:
			mcurve.delt = 0.5
			mcurve.calc_derivatives()

		if curvature.is_calced:
			curvature.calc_bcurce_curvature(mcurve)

		draw(canva)

def keypress(event, canva):
	#all this is temporary
	if event.char == 'b':
		mcurve.calc_bezier(bsegments)
		draw(canva)
	elif event.char == 'v':
		mcurve.toggle_bcurve_show()
		draw(canva)
	elif event.char == 'd':
		mcurve.delt = 0.5
		mcurve.calc_derivatives()
		draw(canva)
	elif event.char == 's':
		mcurve.toggle_derivated_show()
		draw(canva)
	elif event.char == 'q':
		mcurve.toggle_derivated_show()
		draw(canva)
	elif event.char == 'c':
		curvature.calc_bcurce_curvature(mcurve)
		curvature.show_lines = True
		draw(canva)
	else:
		pass

def draw(canva):
	mcurve.draw(canva)
	curvature.draw(canva)

#MAIN
def main():
	#SHOWING INITIAL INSTRUNCTION ON TERMINAL
	print("Dynamic Bezier Curve Interactor")
	print("Made by:")
	print("\tLeonardo Da Vinci (lvfs)")
	print("\tHeitor Fontes (hfxc)")
	print("\nInstructions:")
	print("\t1. click to add a point")
	print("\t2. press 'b' to calculate and show the bezier curve")
	print("\t3. press 'v' to to toggle the bezier curve view")
	print("\t4. press 'd' to calculate and show the derivaties curves")
	print("\t5. press 's' to toggle the derivaties curves view")
	print("\t6. press 'space' to toggle the control curve view")
	print("\t7. press 'c' to calculate the bezier curve curvature")
	print("\t8. click on a point, hold and drag to move it")
	print("\t9. move the mouse upon a point and press 'del' to delete it")

	global mcurve
	global curvature


	#CREATING CANVA
	tkroot = tk.Tk()
	scrw = tkroot.winfo_screenwidth() #screen width
	scrh = tkroot.winfo_screenheight() #screen height
	width = 400 #window width
	height = 400 #window height
	print("screen resolution: " + str(scrw) + "x" + str(scrh))
	frame = tk.Canvas(tkroot, width=width, height=height)
	# frame = tk.Canvas(tkroot, width=scrw, height=scrh)
	# tkroot.attributes("-fullscreen", True)
	tkroot.bind('<Button-1>', lambda event: onclick(event, canva=frame))
	tkroot.bind("<Key>", lambda event: keypress(event, canva=frame))
	tkroot.bind("<B1-Motion>", lambda event: onmove(event, canva=frame))
	tkroot.bind("<ButtonRelease-1>", stopMoving)
	tkroot.bind("<Key-space>", lambda event: toggle_control_lines(event, canva=frame))
	tkroot.bind("<Delete>", lambda event: delete(event, canva=frame))
	frame.pack()

	curvature = Curvature(width, height)

	tk.mainloop()

if __name__ == '__main__':
	main()
