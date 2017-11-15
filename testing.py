import flowerplot
import flowers
import pandas as pd
import numpy as np
from math import log, ceil, floor
from datetime import datetime, time, date
from collections import Counter


flower2 = flowers.Line(np.array([i for i in range(8)]), [i**2/10 for i in range(8)], strokewidth=5, color=[38,214,161,1])
flower1 = flowers.Line([-1,0, 1.3, 1.4, 2], [-1, 2, 0, 1.2, 2], markersize=5)
flower3 = flowers.Bar([1,10,3,6], [2,2,2,2])
flower4 = flowers.Bar([-1,5,6,15], [2,2,2,2])
flower5 = flowers.Bar([0,1,2,3,4,5,6,7], np.array([1, 1, 1, 1, 1, 1, 1, 2]))
flower7 = flowers.Bar([0,1,2,3,4,5,6,7], [1, 1, 1, 1, 1, 1, 1, 2])
flower8 = flowers.Bar([0,1,2,3,4,5,6,7], [1, 1, 1, 1, 1, 1, 1, 2])
flower6 = flowers.Bar([1, 2, 3], [-3,3,-3])

fp = flowerplot.FlowerPlot(flowers=[
	#flower1,
	flower2,
	flower3,
	flower4,
	flower5,
	flower6
	], margins=[100,100,100,100])

fp.save("tests/img/sample.svg")

"""

def rounded_ticks(a, b, ticks):
    span = floor(b) - ceil(a)
    dx = (10**floor(log(span, 10)))/10
    start = dx
    while start < ceil(a):
    	start += dx

    jump = dx*floor(span/ticks/dx)
    return [start + i*jump for i in range(ticks)]


def precise_ticks(a, b, ticks):
	if ticks == 0:
		pass
	elif ticks == 1:
		return [(b-a)/2]
	elif ticks > 1:
		return [a+(b-a)*i/float(ticks-1) for i in range(ticks)]

print(precise_ticks(2, 10, 9))


"""


