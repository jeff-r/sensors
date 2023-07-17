import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

print(ser.name)         # check which port was really used

while True:
  str = ser.readline().decode('Ascii').replace("\r\n", "")
  print(str)

ser.close()

