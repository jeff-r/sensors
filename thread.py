import time
import serial
import threading
import numpy as np
import read_csv_data as rcd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print(ser.name)         # check which port was really used

N = 1000
samples = []
for n in range(N):
  samples.append([0,0,0])

# print('samples:', samples)
def add_data(line):
  global samples
  if len(line) == 3:
    samples.append(line)

continue_reading = True
def read_data(filename):
  while continue_reading:
    str = ser.readline().decode('Ascii').replace("\r\n", "")
    line = rcd.transform_line(str)
    add_data(line)

def tick(n):
  print("hi", samples[-10:])

def recent_values():
  return list(map(val, samples[-N:]))

def val(point):
  return point[2]

print('recent_values:', recent_values())

# Create a figure and axis object
fig, ax = plt.subplots()

# Define the x axis
x = np.arange(0, N, 1)

# Create a line plot
line, = ax.plot(x, recent_values())

# Define the update function for the animation
def update(n):
    # Shift the x and y data
    vals = recent_values()
    ax.set_ylim(np.min(vals), np.max(vals))
    line.set_data(x, recent_values())
    return line,

def main():
  n = 0
  thread = threading.Thread(target=read_data, args=('data/foo.csv',), daemon=True)
  thread.start()
  # Create the animation object
  ani = animation.FuncAnimation(fig, update, frames=50, interval=50)

  # Show the plot
  plt.show()

try:
  print('hi')
  main()
except KeyboardInterrupt:
  continue_reading = False
  ser.close()
  print('bye', samples)
