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
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')
sampling_frequency = 1.0 / 50.0

def plot_fft(arr, label):
  fft = np.fft.fft(arr)
  power_spectrum = np.abs(fft) ** 2
  # power_spectrum = np.abs(fft)
  freqs = np.fft.fftfreq(len(arr), sampling_frequency).astype(float)
  
  power_spectrum[0] = 0
  power_spectrum[1] = 0
  power_spectrum[2] = 0

  ax.plot(freqs[:len(freqs)//2+1], power_spectrum[:len(freqs)//2+1])
  # ax.plot(freqs[:len(freqs)//2+1], power_spectrum[:len(freqs)//2+1], label=label)

# plot_fft(zs, label='Z')
# plot_fft(xs, label='X')
plot_fft(ys, label='Y')
# ax.legend()
plt.show()

