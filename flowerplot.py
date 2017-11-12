import xml.etree.ElementTree as et
import numpy as np
import flowers as fl
from collections import Counter
from styling import color_cycles

svg_config = {
	'style':'fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;',
	'version':'1.1',
	'xmlns':'http://www.w3.org/2000/svg',
	'xmlns:xlink':'http://www.w3.org/1999/xlink',
	'xml:space':'preserve',
}

num_colors = len(color_cycles)
print(color_cycles)

class FlowerPlot(object):
	def __init__(self, flowers=[], width=1000, height=1000, margins=[100, 100, 100, 100], **kwargs):
		self.flowers = flowers
		self.width = width
		self.height = height
		self.margin_top = margins[0]
		self.margin_bottom = margins[1]
		self.margin_left = margins[2]
		self.margin_right = margins[3]
		#self.max_x_count = np.max(len(flower.xdata) for flower in flowers)
		
		self.svg = et.Element('svg')
		self.svg.set('viewBox', f"0 0 {width} {height}")
		for attr, value in svg_config.items():
			self.svg.set(f"{attr}", f"{value}")

		self.x_dtypes = set([flower.x_dtype for flower in flowers])
		self.y_dtypes = set([flower.y_dtype for flower in flowers])

		self.lines = [l for l in flowers if isinstance(l, fl.Line)]
		self.scatters = [s for s in flowers if isinstance(s, fl.Scatter)]
		self.bars = [b for b in flowers if isinstance(b, fl.Bar)]

		if len(self.x_dtypes) > 1:
			raise Exception("Incompatible data types have been specified for at least one axis.")

		self.plant()


	def plant(self):
		if len(self.x_dtypes) == 1 and len(self.y_dtypes) == 1 and 'numeric' in self.x_dtypes and 'numeric' in self.y_dtypes:
			xmin = np.min([np.min(flower.xdata) for flower in self.flowers])
			xmax = np.max([np.max(flower.xdata) for flower in self.flowers])
			ymin = np.min([np.min(flower.ydata) for flower in self.flowers])
			ymax = np.max([np.max(flower.ydata) for flower in self.flowers])

			if len(self.bars) > 0:#any(isinstance(flower, fl.Bar) for flower in self.flowers):
				if ymax < 0:
					ymax = 0
				elif ymin > 0:
					ymin = 0

			#max_x_count = np.max([len(flower.xdata) for flower in self.flowers])
			w = self.width - self.margin_left - self.margin_right
			h = self.height - self.margin_top - self.margin_bottom

			color_index = 0

			for flower in self.lines:
				flower.color = color_cycles[color_index%num_colors]
				color_index += 1
				c = flower.water(flower.xdata, flower.ydata, w, h, xmin, xmax, ymin, ymax)
				c.set('transform', f"translate({self.margin_left},{self.margin_top})")
				self.svg.append(c)

			for flower in self.scatters:
				flower.color = color_cycles[color_index%num_colors]
				color_index += 1
				c = flower.water(flower.xdata, flower.ydata, w, h, xmin, xmax, ymin, ymax)
				c.set('transform', f"translate({self.margin_left},{self.margin_top})")
				self.svg.append(c)

			if self.bars:
				olive_x = []
				for bar in self.bars:
					olive_x += list(set(bar.xdata))
				min_x_dist = np.min(np.diff(sorted(list(set(olive_x)))))
				max_repeat = Counter(olive_x).most_common(1)[0][1]
				for i, flower in enumerate(self.bars):
					flower.color = color_cycles[color_index%num_colors]
					color_index += 1
					c = flower.water(flower.xdata, flower.ydata, w, h, xmin, xmax, ymin, ymax, len(self.bars), i, max_repeat, min_x_dist)
					c.set('transform', f"translate({self.margin_left},{self.margin_top})")
					self.svg.append(c)
		else:
			pass

	def save(self, filepath):
		with open(filepath, 'w') as f:
			f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">")
			f.write(str(et.tostring(self.svg).decode('utf-8')))


