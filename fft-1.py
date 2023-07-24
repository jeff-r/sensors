import numpy as np
import matplotlib.pyplot as plt
import sys
import read_csv_data as rcd

y = rcd.read_data(sys.argv[1])
arr = np.array(y)
xs = arr[:,0]
ys = arr[:,1]
zs = arr[:,2]
fig, ax = plt.subplots()

def plot_fft(arr, label):
  fft = np.fft.fft(arr)
  power_spectrum = np.abs(fft) ** 2
  freqs = np.fft.fftfreq(len(arr), 0.05)
  
  ax.plot(freqs, power_spectrum, label=label)
  # ax.xlabel('Frequency (Hz)')
  # ax.ylabel(label)

plot_fft(ys, label='Z')
plot_fft(ys, label='X')
plot_fft(ys, label='Y')
ax.legend()
plt.show()

