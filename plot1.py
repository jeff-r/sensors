import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import read_csv_data as rcd

def normalized(vals, N):
  cumsum = np.cumsum(np.insert(vals, 0, 0)) 
  return (cumsum[N:] - cumsum[:-N]) / float(N)

def runningMeanFast(x, N):
  return np.convolve(x, np.ones((N,))/N, mode='valid')[(N-1):]

def normalize(arr):
  ave = np.sum(arr) / len(arr)
  return arr - ave

def smooth_data(arr):
  arr = normalize(arr)
  arr = np.absolute(arr)
  arr = runningMeanFast(arr, N)
  return arr

fig, ax = plt.subplots()
y = rcd.read_data(sys.argv[1])
arr = np.array(y)
xs = arr[:,0]
ys = arr[:,1]
zs = arr[:,2]
N = 100

# xs = smooth_data(xs)
# ys = smooth_data(ys)
# zs = smooth_data(zs)

ax.plot(xs, label='X')
ax.plot(ys, label='Y')
ax.plot(zs, label='Z')
ax.legend()
plt.show()

