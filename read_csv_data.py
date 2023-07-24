import numpy as np
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
  lines = list(lines)
  lines = list(filter(lambda vals: len(vals) == 3, lines))
  return lines

