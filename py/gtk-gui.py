#!/usr/bin/env python3

# sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
# sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 
# pip3 install pycairo
# pip3 install PyGObject

# Load Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# When the application is launched…
def on_activate(app):
    # … create a new window…
    win = Gtk.ApplicationWindow(application=app)
    # … with a button in it…
    btn = Gtk.Button(label='Hello, World!')
    # … which closes the window when clicked
    btn.connect('clicked', lambda x: win.close())
    win.add(btn)
    win.show_all()

# Create a new application
app = Gtk.Application(application_id='com.example.GtkApplication')
app.connect('activate', on_activate)

# Run the application
app.run(None)