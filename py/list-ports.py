#!/usr/bin/env python3

"""
  Tauno Erik
  15.10.2020
"""

import serial # pip3 install pyserial
import serial.tools.list_ports

def find_ports():
  ports = list(serial.tools.list_ports.comports())
  for port in ports:
    print("{} \t {} -- {}".format(port[0],port[1],port[2]))
    #print(port[0]) # /dev/ttyACM0
    #print(port[1]) # USB2.0-Serial
    #print(port[2]) # USB VID:PID=2341:0043 SER=9563430343235150C281 LOCATION=1-1.4.4:1.0

if __name__ == '__main__':
  find_ports()