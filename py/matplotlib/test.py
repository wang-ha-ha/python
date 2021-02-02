import numpy as np
import math
import matplotlib.pyplot as plt
#sin & cos曲线
x = np.arange(0, 10, 0.1)
y1 = x * x
y2 = 2 ** x
plt.plot(x,y1,label="x^2")
plt.plot(x,y2,label="2^x",linestyle = "--")
plt.xlabel("x")
plt.ylabel("y")
plt.title('sin & cos')
plt.legend()   #打上标签
plt.show()
