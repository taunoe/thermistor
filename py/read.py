#!/usr/bin/env python3

"""
  Tauno Erik
  17.10.2020
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
import argparse
import os
import re
import serial # pip3 install pyserial
import serial.tools.list_ports
import sys




def find_numbers(str):
  """
  Extract all the numbers from the given string
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

  filename = "log.csv"
  flag_file_open = False

  if args.log:
    path = os.getcwd() + '/' # absolute path
    print("Log data: {}{}".format(path, filename))
  
  # Open serial
  ser = serial.Serial(args.port, args.baudrate)

  while ser.is_open:
    try:
      incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
      print("{}".format(incoming_data))
      numbers = find_numbers(incoming_data)
      #print(numbers)
      if args.log:
        file = open(filename, "a") # append
        flag_file_open = True
        file.write(str(numbers[2] + ",")) # Write average 
        file.close()
    except KeyboardInterrupt:
      # Exit when CTRL-C pressed
      print('CTRL-C detected.')
      ser.close()
      if flag_file_open:
        file.close()
      exit(0)
      

if __name__ == '__main__':
  main(sys.argv)