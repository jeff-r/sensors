import numpy as np
import matplotlib.pyplot as plt
import sys
import read_csv_data as rcd

y = rcd.read_data(sys.argv[1])
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

