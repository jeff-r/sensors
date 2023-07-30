import time
import math
import serial
import threading
import numpy as np
import read_csv_data as rcd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

def now_formatted():
  return datetime.now().strftime("%y-%m-%d-%H-%M-%S")

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print(ser.name)         # check which port was really used

N = 1000
samples = []
for n in range(N):
  samples.append([0,0,0])

def add_data(line):
  global samples
  if len(line) == 3:
    samples.append(line)

continue_reading = True
def read_data(filename):
  while continue_reading:
    try:
      str = ser.readline()
      str = str.decode('Ascii').replace("\r\n", "")
      line = rcd.transform_line(str)
      add_data(line)
    except AttributeError:
      print('Saw AttributeError')

blackman = np.blackman(N)
def recent_values():
  windowed = blackman*list(map(val, samples[-N:]))
  return windowed

def val(point):
  return point[1]

sampling_frequency = 1.0 / 50.0

def do_fft():
  recents = recent_values()
  fft = np.fft.fft(recents)
  power_spectrum = np.abs(fft) ** 2
  freqs = np.fft.fftfreq(len(recents), sampling_frequency).astype(float)
  for n in range(20):
    power_spectrum[n] = 0
  return power_spectrum

values = do_fft()
freqs = np.fft.fftfreq(len(values), sampling_frequency).astype(float)

x = freqs[:len(freqs)//2]
values = values[:len(freqs)//2]

# Create a figure and axis object
fig, ax = plt.subplots()

# Create a line plot
# line, = ax.semilogy(x, values)
line, = ax.plot(x, values)

# Window around peak value to use to calculate total power
# Arbitrarily set this to number of samples that make up 1 Hz
# So, find the index of the first frequency bin > 1
power_window = np.where(x > 1.0)[0][0]

def power_at(index, values):
  min = int(index - power_window)
  max = int(index + power_window)
  if min < 0:
    return 0
  return np.trapz(values[min:max], x[min:max])

# Define the update function for the animation
def update(n):
  # Shift the x and y data
  values = do_fft()
  values = values[:len(freqs)//2]
  ax.set_ylim(np.min(values), np.max(values))
  ax.set_xlabel('Frequency (Hz)')
  ax.set_ylabel('Tremor magnitude')
  max_index = np.argmax(values)
  power = power_at(max_index, values)
  print("%.2f" % x[max_index], "%.2f" % np.max(values), "%.2f" % power)
  line.set_data(x, values)
  return line,

def main():
  n = 0
  global data_thread
  data_thread = threading.Thread(target=read_data, args=('data/foo.csv',), daemon=True)
  data_thread.start()
  # Create the animation object
  ani = animation.FuncAnimation(fig, update, frames=50, interval=50)
  print('just called FuncAnimation')

  fig.canvas.mpl_connect('close_event', on_close)
  fig.canvas.mpl_connect('button_press_event', on_click)
  # Show the plot
  plt.show()

def on_click(event):
  print('click')
  plt.savefig('img/' + now_formatted() + '.png')
  file = open('moments.csv', 'a')
  now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
  values = do_fft()
  values = values[:len(freqs)//2]
  max_index = np.argmax(values)
  power = power_at(max_index, values)
  file.write(now + "," + "%.2f" % x[max_index] + ",%.2f" % np.max(values) + ",%.2f" % power + "\n")

def on_close(event):
  print("\n")
  f = open('out.csv', 'w')
  for line in recent_values():
    f.write(str(line))
    f.write("\n")
  f.close

try:
  main()
except KeyboardInterrupt:
  continue_reading = False
  ser.close()
  print(recent_values())
