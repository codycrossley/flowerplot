import flowerplot
import flowers
import pandas as pd
import numpy as np
from math import log, ceil, floor
from datetime import datetime, time, date
from collections import Counter


flower2 = flowers.Line(np.array([i for i in range(8)]), [i**2/10-1 for i in range(8)], strokewidth=5, color=[38,214,161,1])
flower1 = flowers.Line([0, 0.1, 0.2], [-1, 2, 0], markersize=5)
flower3 = flowers.Bar([1,10,3,6], [2,2,2,2])
flower4 = flowers.Bar([-1,5,6,15], [2,2,2,2])
flower5 = flowers.Bar([0,7], np.array([1, 2]))
flower7 = flowers.Bar([0,1,2,3,4,5,6,7], [1, 1, 1, 1, 1, 1, 1, 2])
flower8 = flowers.Bar([0,1,2,3,4,5,6,7], [1, 1, 1, 1, 1, 1, 1, 2])
flower6 = flowers.Scatter([1, 2, 3], [-3,3,-3])

x_config = {
	'show_labels': True,
	'ticks': 4,
	'title': 'UGH',
	'units': 'ugh'
}

y_config = {
	'axis_width': 2,
	'ticks': 4,
	'show_grid': True,
	'zeroline': True,
	'title': 'test',
	'units': 'testttt'
}



fp = flowerplot.FlowerPlot(flowers=[
flower5
	],
	x_axis = x_config,
	y_axis = y_config,
	)

fp.save("tests/img/sample.svg")


