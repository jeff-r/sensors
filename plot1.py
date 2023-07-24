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
  if vals != ['']:
    vals = [vals[0], vals[1], vals[2]]
    # vals = [vals[0], vals[1], vals[2], vals[3]]
  vals = list(map(transform_val, vals))
  # print(vals)
  return vals

def read_data(filename):
  file = open(filename, 'r')
  lines = file.readlines()
  file.close()
  lines = map(transform_line, lines)
  lines = list(lines)
  lines = list(filter(lambda vals: len(vals) == 3, lines))
  return lines

def normalized(vals, N):
  cumsum = np.cumsum(np.insert(vals, 0, 0)) 
  return (cumsum[N:] - cumsum[:-N]) / float(N)

def runningMeanFast(x, N):
  return np.convolve(x, np.ones((N,))/N, mode='valid')[(N-1):]

def normalize(arr):
  ave = np.sum(arr) / len(arr)
  return arr - ave

def massage(arr):
  arr = normalize(arr)
  arr = np.absolute(arr)
  arr = runningMeanFast(arr, N)
  return arr

fig, ax = plt.subplots()
y = read_data(sys.argv[1])
arr = np.array(y)
xs = arr[:,0]
ys = arr[:,1]
zs = arr[:,2]
N = 100

xs = massage(xs)
ys = massage(ys)
zs = massage(zs)

ax.plot(xs)
ax.plot(ys)
ax.plot(zs)
plt.show()

