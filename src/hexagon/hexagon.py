#!/bin/bash

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


import time
import threading
import sys


class Window():
    builder = Gtk.Builder()
    builder.add_from_file("../glade/center.glade")
    window = builder.get_object("Center")
    window.connect("destroy", Gtk.main_quit)
    title = builder.get_object("Titlebar")

    title.set_label("Nachos")

    window.show_all()
    Gtk.main()
