#Bezier curve interactive vizualizer

from curve import Curve
import tkinter as tk
import functools


#FUNCTIONS
def onclick(event, curve, canva):
	curve.add_point(event.x, event.y)
	curve.draw(canva)

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
	else:
		pass


#MAIN
def main():
	mcurve = Curve() #main curve
	mcurve.makeMaster()

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
	frame.pack()
	tk.mainloop()

if __name__ == '__main__':
	main()
