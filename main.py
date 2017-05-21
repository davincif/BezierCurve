#Bézier curve interactive vizualizer

from curve import Curve
import tkinter as tk


#MAIN
def main():
	#GETTING INITIAL POINTS BY TERMINAL
	print("enter the points, or just a dot '.' when you're done")
	baux = True
	mcurve = [] #main curve
	while baux:
		print("points ", mcurve)
		x = str(input("\nx = "))
		if x != '.':
			y = str(input("y = "))
			if y != '.':
				mcurve = mcurve + [float(x), float(y)]
			else:
				baux = False
		else:
			baux = False
	print("points get ", mcurve, end='\n\n\n')
	mcurve = Curve(mcurve)

	#CREATING CANVA
	tkroot = tk.Tk()
	scrw = tkroot.winfo_screenwidth() #screen width
	scrh = tkroot.winfo_screenheight() #screen height
	print("resolution " + str(scrw) + "x" + str(scrh))
	frame = tk.Canvas(tkroot, width=scrw, height=scrh)
	tkroot.attributes("-fullscreen", True)
	frame.pack()

	#DUNNO YET ^^
	# frame.create_polygon(mcurve.printable(), outline="black", width=3)
	mcurve.draw(frame)

	tk.mainloop()

if __name__ == '__main__':
	main()

#will help:
#http://www.python-course.eu/tkinter_canvas.php
#http://effbot.org/tkinterbook/canvas.htm

#good start [100, 600, 500, 200, 800, 350, 1000, 700]