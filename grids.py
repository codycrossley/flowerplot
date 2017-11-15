import xml.etree.ElementTree as et
import numpy as np
from styling import color_cycles
from math import floor, ceil, log

svg_config = {
	'style':'fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;',
	'version':'1.1',
	'xmlns':'http://www.w3.org/2000/svg',
	'xmlns:xlink':'http://www.w3.org/1999/xlink',
	'xml:space':'preserve',
}

gridline_config = {
	'strokewidth': 1,
	'color': [219, 216, 215, 1],
}

axis_config = {
	'strokewidth': 2,
	'color': [119, 116, 115, 1],
}

x_config = {
	'show': True,
	'ticks': 4,
	'zeroline': True,
}

y_config = {
	'show': True,
	'ticks': 4,	
	'zeroline': True,
}

class Grid(object):
	def __init__(self, svg_package, x_axis=x_config, y_axis=y_config, margins=[50, 50, 50, 50], **kwargs):
		#self.show_x = kwargs.get('show_x', True)
		#self.show_y = kwargs.get('show_y', True)
		self.x_config = x_axis
		self.y_config = y_axis

		self.grid = et.Element('svg')
		self.plot = svg_package['svg_element']

		self.margin_top = margins[0]
		self.margin_bottom = margins[1]
		self.margin_left = margins[2]
		self.margin_right = margins[3]

		self.xdata = svg_package['distinct_xdata']
		self.ydata = svg_package['distinct_ydata']
		self.x_dtypes = svg_package['x_dtypes']
		self.y_dtypes = svg_package['y_dtypes']
		self.plot_width = svg_package['width']
		self.plot_height = svg_package['height']
		self.plot_margins = svg_package['margins']

		self.grid.set('viewBox', f"0 0 {self.plot_width+self.margin_left+self.margin_right} {self.plot_height+self.margin_top+self.margin_bottom}")
		for attr, value in svg_config.items():
			self.grid.set(f"{attr}", f"{value}")

		g = et.Element('g')
		g.set('transform', f"translate({self.margin_left},{self.margin_top})")

		if x_axis['show']:
			g.append(self.construct_x())

		if y_axis['show']:
			g.append(self.construct_y())

		for e in self.plot:
			g.append(e)

		self.grid.append(g)

	def grid_as_element(self):
		return self.grid

	def construct_x(self):
		if 'numeric' in self.x_dtypes and len(self.x_dtypes) == 1:
			xmin = np.min(self.xdata)
			xmax = np.max(self.xdata)
			ticks = self.x_config['ticks']

			x_grid_labels = precise_ticks(xmin, xmax, ticks)
			x_positions = [[(self.plot_width-self.plot_margins[2]-self.plot_margins[3])*(x - xmin)/(xmax-xmin), x] for x in x_grid_labels]
			gridlines = et.Element('g')

			for x in x_positions:
				line = GridLine(M=[x[0], self.plot_height-self.plot_margins[0]-self.plot_margins[1]], L=[x[0], 0])
				gridlines.append(line.line_as_element())

			if xmin <= 0 <= xmax and self.x_config['zeroline']:
				xpos = (self.plot_width-self.plot_margins[2]-self.plot_margins[3])*(0 - xmin)/(xmax-xmin)
				axis = Axis(M=[xpos, self.plot_height-self.plot_margins[0]-self.plot_margins[1]], L=[xpos, 0])
				gridlines.append(axis.axis_as_element())

			gridlines.set('transform', f"translate({self.plot_margins[2]},{self.plot_margins[0]})")
			return gridlines

	def construct_y(self):
		if 'numeric' in self.y_dtypes and len(self.y_dtypes) == 1:
			ymin = np.min(self.ydata)
			ymax = np.max(self.ydata)
			ticks = self.y_config['ticks']

			y_grid_labels = precise_ticks(ymin, ymax, ticks)
			print(y_grid_labels)
			y_positions = [[(self.plot_height-self.plot_margins[0]-self.plot_margins[1])*(y - ymin)/(ymax-ymin), y] for y in y_grid_labels]
			gridlines = et.Element('g')

			for y in y_positions:
				if y[1] == 0:
					pass
				else:
					line = GridLine(M=[0, self.plot_height-self.plot_margins[0]-self.plot_margins[1]-y[0]], L=[self.plot_width-self.plot_margins[2]-self.plot_margins[3], self.plot_height-self.plot_margins[0]-self.plot_margins[1]-y[0]])
					gridlines.append(line.line_as_element())
			
			if ymin <= 0 <= ymax and self.y_config['zeroline']:
				ypos = (self.plot_height-self.plot_margins[0]-self.plot_margins[1])*(0-ymin)/(ymax-ymin)
				axis = Axis(M=[0, self.plot_height-self.plot_margins[0]-self.plot_margins[1]-ypos], L=[self.plot_width-self.plot_margins[2]-self.plot_margins[3], self.plot_height-self.plot_margins[0]-self.plot_margins[1]-ypos])
				gridlines.append(axis.axis_as_element())
			
			gridlines.set('transform', f"translate({self.plot_margins[2]},{self.plot_margins[0]})")
			return gridlines


class GridLine(object):
	def __init__(self, M=[0,0], L=[0,0], **kwargs):
		self.gridline = et.Element('path')
		self.gridline.set('d', f"M{M[0]},{M[1]} L{L[0]},{L[1]}")
		self.gridline.set('fill', 'none')

		strokewidth = kwargs.get('strokewidth', gridline_config['strokewidth'])
		color = kwargs.get('color', gridline_config['color'])

		self.gridline.set('stroke-width', f"{strokewidth}")
		self.gridline.set('stroke', f"rgb({color[0]},{color[1]},{color[2]})")
		self.gridline.set('stroke-opacity', f"{color[3]}")

	def line_as_element(self):
		return self.gridline

	def line_as_string(self):
		return et.tostring(self.gridline).decode('utf-8')


class Axis(object):
	def __init__(self, M=[0,0], L=[0,0], **kwargs):
		self.axis = et.Element('path')
		self.axis.set('d', f"M{M[0]},{M[1]} L{L[0]},{L[1]}")
		self.axis.set('fill', 'none')

		strokewidth = kwargs.get('strokewidth', axis_config['strokewidth'])
		color = kwargs.get('color', axis_config['color'])

		self.axis.set('stroke-width', f"{strokewidth}")
		self.axis.set('stroke', f"rgb({color[0]},{color[1]},{color[2]})")
		self.axis.set('stroke-opacity', f"{color[3]}")

	def axis_as_element(self):
		return self.axis

	def axis_as_string(self):
		return et.tostring(self.axis).decode('utf-8')






def rounded_ticks(a, b, ticks):
    span = floor(b) - ceil(a)
    dx = (10**floor(log(span, 10)))/10
    start = dx
    while start < ceil(a):
    	start += dx

    jump = dx*floor(span/ticks/dx)
    print([start + i*jump for i in range(ticks)])
    return [start + i*jump for i in range(ticks)]

def precise_ticks(a, b, ticks):
	if ticks == 0:
		pass
	elif ticks == 1:
		return [(b-a)/2]
	elif ticks > 1:
		return [a+(b-a)*i/float(ticks-1) for i in range(ticks)]



