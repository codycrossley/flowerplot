import xml.etree.ElementTree as et
import numpy as np
from . styling import color_cycles, x_config, y_config
from math import floor, ceil, log
from decimal import Decimal

svg_config = {
	'style':'fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;',
	'version':'1.1',
	'xmlns':'http://www.w3.org/2000/svg',
	'xmlns:xlink':'http://www.w3.org/1999/xlink',
	'xml:space':'preserve',
}

def humanreadable(n, suffix='', precision=1, close=False):
    prefixes = ['', 'K', 'M', 'B', 'T']
    tempnum = n
    for prefix in prefixes:      
        if abs(tempnum) < 1000:
            return f"{'%.1f'%tempnum} {prefix}{suffix}"
        else:
            tempnum /= 1000
        
    return "{:.1E}".format(Decimal(n))


class Grid(object):
	def __init__(self, svg_package, x_axis, y_axis, margins=[50, 100, 100, 50], **kwargs):
		self.x_config = {**x_config, **x_axis}
		self.y_config = {**y_config, **y_axis}

		#{attr:x_config[attr] for attr in x_config if attr not in x_axis}

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
		if self.x_config['show']:
			g.append(self.construct_x())
		if self.y_config['show']:
			g.append(self.construct_y())
		for e in self.plot:
			g.append(e)
		self.grid.append(g)

	def grid_as_element(self):
		return self.grid

	def construct_x(self):
		ticks=self.x_config['ticks']
		x_grid = et.Element('g')

		if self.x_config['show_title']:
			title = et.Element('text')
			if self.x_config['units']:
				title.text = f"{self.x_config['title']} ({self.x_config['units']})"
			else:
				title.text = f"{self.x_config['title']}"
			title.set('font-size', f"{self.x_config['title_font_size']}")
			title.set('text-anchor', 'middle')
			title.set('x', f"{self.margin_left + self.plot_width/2}")
			title.set('y', f"{self.margin_top + self.plot_height + self.margin_bottom - self.x_config['title_font_size']}")
			self.grid.append(title)

		if len(self.x_dtypes) == 1:#if 'numeric' in self.x_dtypes and len(self.x_dtypes) == 1:
			if 'numeric' in self.x_dtypes:
				xmin = np.min(self.xdata)
				xmax = np.max(self.xdata)
				x_grid_labels = precise_ticks(xmin, xmax, ticks)
				if ticks > 0:
					x_positions = [[(self.plot_width-self.plot_margins[2]-self.plot_margins[3])*(x - xmin)/(xmax-xmin), x] for x in x_grid_labels]
				else:
					x_positions = []
			elif 'string' in self.x_dtypes:
				xmin = 0
				xmax = self.plot_width #This comes from the svg package; it's defined as the default width of a graph with string x_dtypes
				x_grid_labels = precise_ticks(0, self.plot_width, len(self.xdata))
				if len(self.xdata) > 0:
					x_positions = [[(self.plot_width-self.plot_margins[2]-self.plot_margins[3])*(x - xmin)/(xmax-xmin), x] for x in x_grid_labels]
				else:
					x_positions = []


			if self.x_config['show_grid'] and ticks > 0:
				for x in x_positions:
					line = GridLine(
						M=[x[0], self.plot_height-self.plot_margins[0]-self.plot_margins[1]], 
						L=[x[0], 0], 
						color=self.x_config['grid_color'],
						strokewidth=self.x_config['grid_width'])
					x_grid.append(line.line_as_element())
			
			if xmin <= 0 <= xmax and self.x_config['zeroline']:
				xpos = (self.plot_width-self.plot_margins[2]-self.plot_margins[3])*(0 - xmin)/(xmax-xmin)
				axis = Axis(
					M=[xpos, self.plot_height-self.plot_margins[0]-self.plot_margins[1]], 
					L=[xpos, 0], 
					color=self.x_config['axis_color'],
					strokewidth=self.x_config['axis_width'])
				x_grid.append(axis.axis_as_element())

			if self.x_config['show_labels'] and ticks > 0:
				labels = et.Element('g')

				if 'numeric' in self.x_dtypes:
					for i, label in enumerate(x_grid_labels):
						text = et.Element('text')
						text.text = f"{humanreadable(label)}"
						text.set('x', f"{self.margin_left + self.plot_margins[2] + x_positions[i][0]}")
						text.set('y', f"{self.margin_top + self.plot_height - self.plot_margins[1] + 2*self.x_config['font_size']}")
						text.set('text-anchor', 'middle')
						text.set('font-size', f"{self.x_config['font_size']}")
						labels.append(text)
					
				elif 'string' in self.x_dtypes:
					for i, label in enumerate(self.xdata):
						text = et.Element('text')
						text.text = f"{label}"
						text.set('x', f"{self.margin_left + self.plot_margins[2] + x_positions[i][0]}")
						text.set('y', f"{self.margin_top + self.plot_height - self.plot_margins[1] + 2*self.x_config['font_size']}")
						text.set('text-anchor', 'middle')
						text.set('font-size', f"{self.x_config['font_size']}")
						labels.append(text)

				self.grid.append(labels)

			x_grid.set('transform', f"translate({self.plot_margins[2]},{self.plot_margins[0]})")
			return x_grid

	def construct_y(self):
		ticks = self.y_config['ticks']
		y_grid = et.Element('g')

		if self.y_config['show_title']:
			title = et.Element('text')
			if self.y_config['units']:
				title.text = f"{self.y_config['title']} ({self.y_config['units']})"
			else:
				title.text = f"{self.y_config['title']}"
			title.set('font-size', f"{self.y_config['title_font_size']}")
			title.set('text-anchor', 'middle')
			title.set('x', f"{self.y_config['title_font_size']}")
			title.set('y', f"{self.margin_top + self.plot_height/2}")
			title.set('transform', f"rotate(-90 {self.y_config['title_font_size']} {self.margin_top + self.plot_height/2})")
			self.grid.append(title)

		if 'numeric' in self.y_dtypes and len(self.y_dtypes) == 1:
			ymin = np.min(self.ydata)
			ymax = np.max(self.ydata)
			y_grid_labels = precise_ticks(ymin, ymax, ticks)
			if ticks > 0:
				y_positions = [[(self.plot_height-self.plot_margins[0]-self.plot_margins[1])*(y - ymin)/(ymax-ymin), y] for y in y_grid_labels]
			else:
				y_positions = []

			if self.y_config['show_grid'] and ticks > 0:
				for y in y_positions:
					line = GridLine(
						M=[0, self.plot_height-self.plot_margins[0]-self.plot_margins[1]-y[0]], 
						L=[self.plot_width-self.plot_margins[2]-self.plot_margins[3], self.plot_height-self.plot_margins[0]-self.plot_margins[1]-y[0]], 
						color=self.y_config['grid_color'],
						strokewidth=self.y_config['grid_width'])
					y_grid.append(line.line_as_element())
			
			if ymin <= 0 <= ymax and self.y_config['zeroline']:
				ypos = (self.plot_height-self.plot_margins[0]-self.plot_margins[1])*(0-ymin)/(ymax-ymin)
				axis = Axis(
					M=[0, self.plot_height-self.plot_margins[0]-self.plot_margins[1]-ypos], 
					L=[self.plot_width-self.plot_margins[2]-self.plot_margins[3], self.plot_height-self.plot_margins[0]-self.plot_margins[1]-ypos], 
					color=self.y_config['axis_color'],
					strokewidth=self.y_config['axis_width'])
				y_grid.append(axis.axis_as_element())

			if self.y_config['show_labels'] and ticks > 0:
				labels = et.Element('g')
				for i, label in enumerate(y_grid_labels):
					text = et.Element('text')
					text.text = f"{humanreadable(label)}"
					text.set('x', f"{self.margin_left + self.plot_margins[2] - self.y_config['font_size']}")
					text.set('y', f"{self.margin_top + self.plot_height - self.plot_margins[1] - y_positions[i][0]}")
					text.set('text-anchor', 'end')
					text.set('font-size', f"{self.y_config['font_size']}")
					labels.append(text)
				self.grid.append(labels)

			y_grid.set('transform', f"translate({self.plot_margins[2]},{self.plot_margins[0]})")
			return y_grid


class GridLine(object):
	def __init__(self, M=[0,0], L=[0,0], color=[0,0,0,1], strokewidth=1, **kwargs):
		self.gridline = et.Element('path')
		self.gridline.set('d', f"M{M[0]},{M[1]} L{L[0]},{L[1]}")
		self.gridline.set('fill', 'none')

		#strokewidth = kwargs.get('strokewidth', gridline_config['strokewidth'])
		#color = kwargs.get('color', gridline_config['color'])

		self.gridline.set('stroke-width', f"{strokewidth}")
		self.gridline.set('stroke', f"rgb({color[0]},{color[1]},{color[2]})")
		self.gridline.set('stroke-opacity', f"{color[3]}")

	def line_as_element(self):
		return self.gridline

	def line_as_string(self):
		return et.tostring(self.gridline).decode('utf-8')


class Axis(object):
	def __init__(self, M=[0,0], L=[0,0], color=[0,0,0,1], strokewidth=2, **kwargs):
		self.axis = et.Element('path')
		self.axis.set('d', f"M{M[0]},{M[1]} L{L[0]},{L[1]}")
		self.axis.set('fill', 'none')

		#strokewidth = kwargs.get('strokewidth', axis_config['strokewidth'])
		#color = kwargs.get('color', axis_config['color'])

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



