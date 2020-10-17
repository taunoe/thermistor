#!/usr/bin/env python3

import argparse
import os
from os import path
import re
import serial # pip3 install pyserial
import serial.tools.list_ports
import sys
import tkinter as tk

def find_ports():
  """
    Return list a avaible ports.
  """
  avaible_ports = []
  ports = list(serial.tools.list_ports.comports())
  for port in ports:
    avaible_ports.append(port[0]) # /dev/ttyACM0
  return avaible_ports

def find_numbers(str):
  """
    Extract all the numbers from the given string.
    Return list.
  """
  numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str) 
  return numbers

def read_serial():
  """
    Read Serial port.
    Return average temp.
  """
  try:
    incoming_data = ser.readline()[:-2].decode('ascii')
    numbers = find_numbers(incoming_data)
    average_temp = numbers[2]
  except KeyboardInterrupt:
    print('CTRL-C detected.')
    ser.close()
    exit(0)
  return average_temp

def idle(parent,canvas):
  """
  Update number on canvas.
  """
  data = str(read_serial())
  canvas.itemconfigure("text",text="+"+data+"°C")

  canvas.update()
  parent.after_idle(idle,parent,canvas)


# Check command line arguments
if (len(sys.argv) != 3):
   print("command line: gui.py port baudrate") #/dev/ttyUSB0 4800
   sys.exit()
port = sys.argv[1]
baudrate = int(sys.argv[2])

# kas port on olemas????
if not path.exists(port):
  print("{} not avaible. Try the ones below:". format(port))
  print(find_ports())
  exit(0)

print("Port: {}".format(port))
print("Baudrate: {}".format(baudrate))

# Open serial port
ser = serial.Serial(port, baudrate)

# set up GUI
appname = "Lämmämõõdusk"
WINDOW = 200 # window size

window = tk.Tk()
window.title(appname)
window.bind('q', 'exit')

canvas = tk.Canvas(window, width=2*WINDOW, height=WINDOW, background='white')
canvas.create_text(WINDOW,.5*WINDOW,text="0°C",font=("Ubuntu", 36),tags="text",fill="#525252")
canvas.pack()

# Loop
window.after(100,idle,window,canvas)
window.mainloop()