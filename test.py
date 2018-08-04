import matplotlib.pyplot as plt
import numpy as np
x = np.arange(1,5)
yy = []

for i in x:
    prob = np.power(10.,77 -i) /2.**256
    val = 1. / prob
    yy.append(val)
    print(val)
