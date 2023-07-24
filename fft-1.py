import numpy as np
import matplotlib.pyplot as plt
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
  lines = list(filter(lambda vals: len(vals) == 3, lines))
  return lines

y = read_data(sys.argv[1])
arr = np.array(y)
xs = arr[:,0]
ys = arr[:,1]
zs = arr[:,2]

def plot_fft(arr):
  fft = np.fft.fft(arr)
  power_spectrum = np.abs(fft) ** 2
  freqs = np.fft.fftfreq(len(arr), 0.05)
  
  plt.plot(freqs, power_spectrum)
  plt.xlabel('Frequency (Hz)')
  plt.ylabel('Power')
  plt.show()

plot_fft(ys)

# Generate a signal
# t = np.linspace(0, 1, 1000)
# signal = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 20 * t)
# 
# # Compute the FFT
# fft = np.fft.fft(signal)
# 
# # Compute the power spectrum
# power_spectrum = np.abs(fft) ** 2
# 
# # Compute the frequencies
# freqs = np.fft.fftfreq(len(signal), t[1] - t[0])
# 
# # Plot the power spectrum
# plt.plot(freqs, power_spectrum)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power')
# plt.show()

