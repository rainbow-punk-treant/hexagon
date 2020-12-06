#!/bin/env/ python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


import time
import threading
import sys


class Window(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../glade/center.glade")


        self.window = self.builder.get_object("Center")

        self.provider = Gtk.CssProvider()
        self.screen = self.window.get_screen()
        self.provider.load_from_path("../glade/style.css")
        self.style = self.window.get_style_context()
        self.style.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.lines = 40
        self.c = self.builder.get_object("LineContainer")
        for line in range(self.lines):
            l = Gtk.Entry()
            ls = l.get_style_context()
            ls.add_class("GtkEntry")

            self.c.add(l)

            self.c.show()
        self.window.connect("destroy", Gtk.main_quit)
        self.title = self.builder.get_object("Titlebar")

        self.title.set_label("Nachos")

        self.window.show_all()
    def main(self):
        Gtk.main()
win = Window()
win.main()
