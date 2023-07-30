import time
import math
import serial
import threading
import numpy as np
import read_csv_data as rcd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print(ser.name)         # check which port was really used

N = 500
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

def recent_values():
  return list(map(val, samples[-N:]))

def val(point):
  return point[2]
  # return math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)

sampling_frequency = 1.0 / 50.0

def do_fft():
  recents = recent_values()
  fft = np.fft.fft(recents)
  power_spectrum = np.abs(fft) ** 2
  # power_spectrum = np.abs(fft)
  freqs = np.fft.fftfreq(len(recents), sampling_frequency).astype(float)
  power_spectrum[0] = 0
  power_spectrum[1] = 0
  power_spectrum[2] = 0
  power_spectrum[3] = 0
  power_spectrum[4] = 0
  power_spectrum[5] = 0
  power_spectrum[6] = 0
  return power_spectrum[:len(freqs)//2+1]
  # return fft[:len(freqs)//2+1]

values = do_fft()
freqs = np.fft.fftfreq(len(2*values), sampling_frequency).astype(float)
x = freqs # [:len(freqs)//2+1]

# Create a figure and axis object
fig, ax = plt.subplots()

# Define the x axis
# x = np.arange(0, N, 1)

# Create a line plot
line, = ax.plot(x, values)

# Define the update function for the animation
def update(n):
    # Shift the x and y data
    values = do_fft()
    ax.set_ylim(np.min(values), np.max(values))
    print(np.max(values))
    #ax.set_ylim(0, 1)
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
  # Show the plot
  plt.show()

def on_close(event):
  print("\n")
  f = open('out.csv', 'w')
  for line in recent_values():
    f.write(str(line))
    f.write("\n")
  f.close
  continue_reading = False
  # data_thread.join()
  #ser.close()

try:
  main()
except KeyboardInterrupt:
  continue_reading = False
  ser.close()
  print(recent_values())
