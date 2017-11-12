import flowerplot
import flowers
import pandas as pd
import numpy as np
from datetime import datetime, time, date
from collections import Counter



flower1 = flowers.Scatter([1,2,3,4,5,6,7,8], [np.sin(x) for x in range(8)], color=[0, 0, 255, 0.5], markersize=5)
flower2 = flowers.Line([i for i in range(8)], [i**2/10 for i in range(8)], color=[255, 0, 255, 1], strokewidth=5)
flower3 = flowers.Bar([1,10,3,6], [2,2,-2,2])
flower4 = flowers.Bar([1,5,6,7], [-2,2,2,2])
flower5 = flowers.Bar([1,8], [2,2])
flower6 = flowers.Bar([1, 7, 8], [3,-3,3])
fp = flowerplot.FlowerPlot(flowers=[flower2, flower1, flower3, flower4, flower5,flower6
	], margins=[150,200,200, 150])
fp.save("tests/img/sample.svg")

