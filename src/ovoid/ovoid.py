#!/bin/bash/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
import sys
class Pyramid():
    builder = Gtk.Builder()
    value = ""
    def add_to(self, widget, val, three, four):
        self.value += val
    def boop(self, button):
        if len(sys.argv) < 2 or len(sys.argv) > 2:
            print("If you wish to boop a snoot, please add it as a single string")
        if len(sys.argv) == 2:
            print(self.value)
    def __init__(self):
        self.builder.add_from_file("../glade/speedruneditor.glade")
        self.window = self.builder.get_object("main")
        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)
        self.button = self.builder.get_object("booper")
        self.toBoop = self.builder.get_object("toBoop")
        self.toBoop.connect("insert-text", self.add_to)
        self.button.connect("clicked", self.boop)     
        Gtk.main()
py = Pyramid()