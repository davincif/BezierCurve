#Bezier curve interactive vizualizer

from curve import Curve
import tkinter as tk
import functools

#GLOBAL VARIABLES
global bsegments #segments to construct the bezier curve
bsegments = 35
global movingPoint
movingPoint = None


#FUNCTIONS
def onclick(event, curve, canva):
	global movingPoint

	movingPoint = curve.is_over_point(event.x, event.y)
	if movingPoint is None:
		dpoint, dlines = curve.is_showing_derivatives()
		bpoint, blines = curve.is_showing_bcurve()

		curve.add_point(event.x, event.y)

		if bpoint or blines:
			curve.calc_bezier(bsegments)
			curve.bcurve_show(bpoint, blines)
		if dpoint or dlines:
			curve.delt = 0.5
			curve.calc_derivatives()

		curve.derivatives_show(dpoint, dlines)
		curve.draw(canva)

def onmove(event, curve, canva):
	global movingPoint

	if movingPoint is not None:
		movingPoint.x = event.x
		movingPoint.y = event.y
		dpoint, dlines = curve.is_showing_derivatives()
		bpoint, blines = curve.is_showing_bcurve()

		if bpoint or blines:
			curve.calc_bezier(bsegments)
		if dpoint or dlines:
			curve.delt = 0.5
			curve.calc_derivatives()

		curve.bcurve_show(bpoint, blines)
		curve.derivatives_show(dpoint, dlines)
		curve.draw(canva)


def stopMoving(event):
	global movingPoint

	movingPoint = None

def toggle_control_lines(event, curve, canva):
	if curve.show_lines:
		curve.show_lines = False
	elif curve.show_points:
		curve.show_points = False
	else:
		curve.show_lines = True
		curve.show_points = True
	curve.draw(canva)

def delete(event, curve, canva):
	mp = curve.is_over_point(event.x, event.y) #local moving point
	if mp is not None:
		curve.delete_point(mp)

		dpoint, dlines = curve.is_showing_derivatives()
		bpoint, blines = curve.is_showing_bcurve()
		if bpoint or blines:
			curve.calc_bezier(bsegments)
			curve.bcurve_show(bpoint, blines)
		if dpoint or dlines:
			curve.delt = 0.5
			curve.calc_derivatives()

		curve.draw(canva)

def keypress(event, curve, canva):
	#all this is temporary
	if event.char == 'b':
		curve.calc_bezier(bsegments)
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
	print("\t7. click on a point, hold and drag to move it")
	print("\t8. move the mouse upon a point and press 'del' to delete it")

	#CREATING AND SETTING CURVE
	mcurve = Curve() #main curve
	mcurve.make_master()

	#CREATING CANVA
	tkroot = tk.Tk()
	scrw = tkroot.winfo_screenwidth() #screen width
	scrh = tkroot.winfo_screenheight() #screen height
	print("screen resolution: " + str(scrw) + "x" + str(scrh))
	# frame = tk.Canvas(tkroot, width=400, height=400)
	frame = tk.Canvas(tkroot, width=scrw, height=scrh)
	tkroot.attributes("-fullscreen", True)
	tkroot.bind('<Button-1>', lambda event: onclick(event, curve=mcurve, canva=frame))
	tkroot.bind("<Key>", lambda event: keypress(event, curve=mcurve, canva=frame))
	tkroot.bind("<B1-Motion>", lambda event: onmove(event, curve=mcurve, canva=frame))
	tkroot.bind("<ButtonRelease-1>", stopMoving)
	tkroot.bind("<Key-space>", lambda event: toggle_control_lines(event, curve=mcurve, canva=frame))
	tkroot.bind("<Delete>", lambda event: delete(event, curve=mcurve, canva=frame))
	frame.pack()
	tk.mainloop()

if __name__ == '__main__':
	main()
