import time
import serial
import threading
import numpy as np
import read_csv_data as rcd

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print(ser.name)         # check which port was really used

samples = []
print('samples:', samples)
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

def main():
  n = 0
  thread = threading.Thread(target=read_data, args=('data/foo.csv',), daemon=True)
  thread.start()
  while True:
    n += 1
    tick(n)
    time.sleep(1)

try:
  main()
except KeyboardInterrupt:
  continue_reading = False
  ser.close()
  print('bye', samples)
