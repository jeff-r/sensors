import time
import threading
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print(ser.name)         # check which port was really used

continue_reading = True
def read_data(filename):
  while continue_reading:
    str = ser.readline().decode('Ascii').replace("\r\n", "")
    print(str)

def tick(n):
  print("hi", n)

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
  print('bye')
