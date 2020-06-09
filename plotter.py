import glob
from matplotlib import pyplot as plt
import numpy
import re

for fname in glob.glob("ratios/ratio_*.txt"):
    f = open(fname,'r')
    input = f.read()
    input = re.sub(r'[^0-9 ]', '', input)
    y = numpy.array([int(i) for i in input.split(' ')[1:]])
    x = numpy.array([_ for _ in range(len(y))])
    plt.figure(fname)
    plt.title(fname[])
    plt.plot(x,y)
    print(numpy.sum(y))

plt.show()
