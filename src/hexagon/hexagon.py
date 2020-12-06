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
        self.lineContent = []
        self.lineCount = 0
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../glade/center.glade")


        self.window = self.builder.get_object("Center")
        
        self.provider = Gtk.CssProvider()
        self.screen = self.window.get_screen()
        self.provider.load_from_path("../glade/style.css")
        self.style = self.window.get_style_context()
        self.style.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.lines = 28
        self.c = self.builder.get_object("LineContainer")
        self.line = self.builder.get_object("Line")
        output = ""
        l = ""
        #file = open("../templates/splash", "r")
        #lines = file.readlines()
        for i in range(self.lines):
            if i < self.lines:
                file = open("../templates/atLine", "r")
                l += file.readline()
                file.close()
                self.lineContent.append(l)
                output += l + str("\n")
        #self.line.set_text(output)
        #self.line.connect("button-press-event", self.onClick)
        self.c.add(self.line)
        self.c.show()
        self.window.connect("destroy", Gtk.main_quit)
        self.title = self.builder.get_object("Titlebar")

        self.title.set_label("Nachos")
        self.window.show_all()
        for i in range(self.lines):
            end = self.onClick()
            if end :
                break
            self.c.show()
            self.window.show_all()
            time.sleep(0.01)
        print(len(self.lineContent))

    def onClick(self):
        if self.lineCount >= 28:
            print(len(self.lineContent))
            return True

        added = Gtk.Entry()
        added.style = added.get_style_context()
        added.style.add_class("GtkEntry")
        line = self.builder.get_object("Line")
        #added.connect("button-press-event", self.onClick)
        added.set_text(line.get_text())
        self.c.add(added)
        self.c.show()
        self.lineCount += 1
        self.window.show_all()
        return False
    def main(self):
        Gtk.main()
win = Window()
win.main()
