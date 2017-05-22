#Bézier curve interactive vizualizer

from curve import Curve
import tkinter as tk
import functools


#FUNCTIONS
def onclick(event, curve, canva):
	curve.add_point(event.x, event.y)
	curve.draw(canva)

#MAIN
def main():
	mcurve = Curve() #main curve
	mcurve.makeMaster()

	#CREATING CANVA
	tkroot = tk.Tk()
	scrw = tkroot.winfo_screenwidth() #screen width
	scrh = tkroot.winfo_screenheight() #screen height
	print("resolution " + str(scrw) + "x" + str(scrh))
	# frame = tk.Canvas(tkroot, width=400, height=400)
	frame = tk.Canvas(tkroot, width=scrw, height=scrh)
	tkroot.attributes("-fullscreen", True)
	tkroot.bind('<Button-1>', lambda event : onclick(event, curve=mcurve, canva=frame))
	frame.pack()
	tk.mainloop()

if __name__ == '__main__':
	main()

#will help:
#http://www.python-course.eu/tkinter_canvas.php
#http://effbot.org/tkinterbook/canvas.htm