#!/usr/bin/env python3

"""
  Tauno Erik
  15.10.2020
  Read and log data to csv file

  Usage: python3 ./read.py /dev/ttyACM0 9600
  baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                        '74880','115200','230400','250000','500000','1000000','2000000']

  Links:
  https://docs.python.org/3.9/library/argparse.html#module-argparse
  https://docs.python.org/3.7/howto/argparse.html#id1
  https://www.devdungeon.com/content/python-catch-sigint-ctrl-c
  https://pythonhosted.org/pyserial/shortintro.html
"""

import serial # pip3 install pyserial
import serial.tools.list_ports
import os
import sys
import argparse
import re


def find_numbers(str):
  """
  Function to extract all the numbers from the given string
  https://www.regular-expressions.info/floatingpoint.html
  """
  numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str) 
  return numbers


def main(argv):
  # commandline argument parser
  parser = argparse.ArgumentParser()

  # Required arguments
  parser.add_argument("port", help="Serial port to open.")  
  parser.add_argument("baudrate", type=int, help="Baudrate speed.")

  # Optional arguments
  parser.add_argument("-l","--log", help="Log data to file", action="store_true")

  args = parser.parse_args()

  print("Port = {}".format(args.port))
  print("Baudrate = {}".format(args.baudrate))

  if args.log:
    # absolute path
    path = os.getcwd() + '/'
    file = 'log.csv' # TODO: add time

    print("Log data: {}{}".format(path, file))
  
  # Open serial
  ser = serial.Serial(args.port, args.baudrate)

  while ser.is_open:
    try:
      incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
      print("{}".format(incoming_data))
      numbers = find_numbers(incoming_data)
      print(numbers)
    except KeyboardInterrupt:
      # Exit when CTRL-C pressed
      print('CTRL-C detected.')
      ser.close()
      exit(0)
      

if __name__ == '__main__':
  main(sys.argv)