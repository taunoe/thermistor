#!/usr/bin/env python3

# sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
# sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 
# pip3 install pycairo
# pip3 install PyGObject

# https://stackoverflow.com/questions/31162398/create-a-radio-action-in-a-gtk-popovermenu
# https://stackoverflow.com/questions/31012645/properly-structure-and-highlight-a-gtkpopovermenu-using-pygobject

# Load Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Lämmämõõdusk")
        self.set_default_size(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        # HeaderBar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Lämmämõõdusk"
        self.set_titlebar(hb)

        # Menu icon on HeaderBar
        button_settings = Gtk.MenuButton()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_settings.add(image)
        hb.pack_end(button_settings)

        # Button on window center
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked) # signal clicked calls Method
        self.add(self.button)

    # Method
    def on_button_clicked(self, widget):
        print("Hello World")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()