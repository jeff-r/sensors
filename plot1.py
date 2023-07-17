import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys

def transform_val(val):
  if val == '':
    return val
  else:
    return(float(val))

def transform_line(str):
  vals = str.replace("\n", "").split(",")
  return list(map(transform_val, vals))

def read_data(filename):
  file = open(filename, 'r')
  lines = file.readlines()
  file.close()
  lines = map(transform_line, lines)
  lines = list(lines)
  lines = list(filter(lambda vals: len(vals) == 6, lines))
  return lines

fig, ax = plt.subplots()
x = [1, 2, 3]
y = read_data(sys.argv[1])
ax.plot(y)
plt.show()

