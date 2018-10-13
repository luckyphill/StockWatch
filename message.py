import Tkinter as tk
import ttk
from math import log10, floor

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys
import stock

from global_vars import *

def popupmsg(stock, msg):
	popup = tk.Tk()
	popup.wm_title("StockWatch: " + stock.code + " activity")
	label = ttk.Label(popup, text=msg)
	label.pack(pady=10)
	

	f = Figure(figsize=(6,3), dpi=100)
	a = f.add_subplot(111)
	
	data = stock.GetStockData(200)
	close_price = [line[4] for line in data]
	x = list(range(len(close_price)))
	
	l = a.plot(x, close_price, color='black', linewidth = 1.5)#color='#a2bffe')
	a.fill_between(list(range(len(close_price))), close_price, facecolor='#a2bffe', edgecolor = 'none')
	a.tick_params(axis='x',which='both', bottom=False, top=False, labelbottom=False)
	a.set_xlim(0,len(close_price)-1)

	bottom = min(close_price)
	top = max(close_price)
	rng = top - bottom
	delta = round(rng/6, -int(floor(log10(abs(rng/6)))))
	a.set_ylim(max(bottom - delta,0), top + delta)

	a.grid()

	a.spines['top'].set_color((.8,.8,.8))
	a.spines['bottom'].set_color((.8,.8,.8))
	a.spines['left'].set_color((.8,.8,.8))
	a.spines['right'].set_color((.8,.8,.8))

	canvas = FigureCanvasTkAgg(f,popup)
	canvas.show()
	canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	B1 = ttk.Button(popup, text="Got it", command = popup.destroy)
	B1.pack()
	popup.mainloop()
