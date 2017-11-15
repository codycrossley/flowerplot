import xml.etree.ElementTree as et
import numpy as np
import pandas as pd
import numbers
from styling import color_cycles

# 
#
#- numeric: numeric data type
#- datetime: datetime, date, time, Timestamp data type
#- string: string data type
#
#

scatter_config = {
	'color': [38, 214, 161, 1], #[red, green, blue, opacity]
	'markersize': 3,
}

line_config = {
	'color': [38, 214, 161, 1], #[red, green, blue, opacity]
	'strokewidth': 2,
}

bar_config = {
	'color': [38, 214, 161, 1], #[reg, green, blue opacity]
	'barwidth': 0.6,
}

color_cycle_len = len(color_cycles)

class Flower(object):
	def __init__(self, xdata, ydata, **kwargs):
		self.xdata = xdata
		self.ydata = ydata

		if all(isinstance(x, numbers.Number) for x in self.xdata):
			self.x_dtype = 'numeric'
		elif any(isinstance(x, str) for x in self.xdata):
			try:
				self.xdata = [float(x) for x in self.xdata]
				self.x_dtype = 'numeric'
			except (ValueError, TypeError):
				self.xdata = [str(x) for x in self.xdata]
				self.x_dtype = 'string'
		else:
			self.x_dtype = None

		if all(isinstance(y, numbers.Number) for y in self.ydata):
			self.y_dtype = 'numeric'
		elif any(isinstance(y, str) for y in self.ydata):
			raise Exception("All y-axis values must be numeric (for now). At least one value was detected as a string.")
		else:
			self.y_dtype = None

class Scatter(Flower):
	def __init__(self, xdata, ydata, **kwargs):
		super().__init__(xdata, ydata)
		self.color = kwargs.get('color', False)
		if self.color:
			self.assigned_color = True
		else:
			self.color = color_cycles[0]
			self.assigned_color = False
		self.markersize = kwargs.get('markersize', scatter_config['markersize'])


	def water(self, xdata, ydata, width, height, xmin, xmax, ymin, ymax):
		if self.x_dtype == 'numeric':
			x_scaled = [width * (x-xmin) / (xmax-xmin) for x in xdata]
			y_scaled = [height * (y-ymin) / (ymax-ymin) for y in ydata]
			circles = et.Element('g')
			for i,x in enumerate(x_scaled):
				circle = et.Element('circle')
				circle.set('cx', f"{x}")
				circle.set('cy', f"{height-y_scaled[i]}")
				circle.set('r', f"{self.markersize}")
				circle.set('fill', f"rgb({self.color[0]},{self.color[1]},{self.color[2]})")
				circle.set('fill-opacity', f"{self.color[3]}")
				circles.append(circle)
			return circles
		else:
			return None

class Line(Flower):
	def __init__(self, xdata, ydata, **kwargs):
		super().__init__(xdata, ydata)
		self.strokewidth = kwargs.get('strokewidth', line_config['strokewidth'])
		self.color = kwargs.get('color', False)
		if self.color:
			self.assigned_color = True
		else:
			self.color = color_cycles[0]
			self.assigned_color = False

	def water(self, xdata, ydata, width, height, xmin, xmax, ymin, ymax):
		if self.x_dtype == 'numeric':
			x_scaled = [width*(x-xmin)/(xmax-xmin) for x in xdata]
			y_scaled = [height*(y-ymin)/(ymax-ymin) for y in ydata]
			line = et.Element('path')
			line.set('stroke', f"rgb({self.color[0]},{self.color[1]},{self.color[2]})")
			line.set('stroke-opacity', f"{self.color[3]}")
			line.set('stroke-width', f"{self.strokewidth}")
			line.set('fill', 'none')
			d = f"M{x_scaled[0]}, {height-y_scaled[0]}"
			for i,x in enumerate(x_scaled[1:]):
				d += f" L{x}, {height-y_scaled[i+1]}"
			line.set('d', d)
			return line
		else:
			return None

class Bar(Flower):
	def __init__(self, xdata, ydata, **kwargs):
		super().__init__(xdata, ydata)
		self.color = kwargs.get('color', False)
		if self.color:
			self.assigned_color = True
		else:
			self.color = color_cycles[0]
			self.assigned_color = False
		self.barwidth = kwargs.get('barwidth', bar_config['barwidth'])

	def water(self, xdata, ydata, width, height, xmin, xmax, ymin, ymax, numbarcharts, barid, max_repeat, min_x_dist, longest_x, **kwargs):
		barheights = [abs(height*(y)/(ymax-ymin)) for y in ydata]

		if self.x_dtype == 'numeric':
			#xdata_count = len(set(xdata))
			barwidth = max(min(width/longest_x, width*(min_x_dist)/(xmax-xmin))*self.barwidth, 1)/max_repeat
			xpositions = [width*(x-xmin)/(xmax-xmin)  for x in xdata]

			bars = et.Element('g')
			for i,x in enumerate(xpositions):
				bar = et.Element('rect')
				bar.set('stroke', 'none')
				bar.set('fill', f"rgb({self.color[0]},{self.color[1]},{self.color[2]})")
				bar.set('fill-opacity', f"{self.color[3]}")
				bar.set('x', f"{x-(numbarcharts-2*barid)*(barwidth/2)}")
				if ymax == 0:
					yshift = height
				elif ymin == 0:
					yshift = barheights[i]
				else:
					dist_to_zero = abs((height * ymin / (ymax-ymin)))
					yshift = barheights[i] + dist_to_zero  if ydata[i] >= 0 else dist_to_zero
				bar.set('y', f"{height-yshift}")
				bar.set('width', f"{barwidth}")
				bar.set('height', f"{barheights[i]}")
				bars.append(bar)
		elif self.x_dtype == 'string':
			xdata_count = len(set(xdata))
			barwidth = max(min(width/xdata_count, width*(min_x_dist)/(xmax-xmin))*self.barwidth, 1)/max_repeat


		return bars


