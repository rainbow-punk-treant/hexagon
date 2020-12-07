#!/bin/bash/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


import time
import threading
import sys


class Window(Gtk.Window):
    def spawnEditor(self):
        builder = Gtk.Builder()
        builder.add_from_file("../glade/editor.glade")
        editor = self.builder.get_object("editor")
        #editor.show()
        for l in range(self.lines):
            c = self.builder.get_object("Line"+str(l))
            
            c.connect("key-press-event", self.moveNext)
            c.connect("key-press-event", self.movePrevious)
            lab = self.builder.get_object(str(l))
            #Uncomment the following line to get line numbers
            #lab.set_text(str(l))
            lab.show()
        return editor



    def __init__(self):
        Gtk.init()
        #I should use a class for this.
        self.lineContent = []
        self.Lines = []
        self.LineNames = []

        self.lineCount = 0
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../glade/center.glade")
        self.builderEd = Gtk.Builder()
        self.builderEd.add_from_file("../glade/editor.glade")
        self.builderEdd = Gtk.Builder()
        self.builderEdd.add_from_file("../glade/editor.glade")




        self.window = self.builder.get_object("Center")
        #self.window.__init__(self, title='Hexagon Editor')
        self.provider = Gtk.CssProvider()
        self.screen = self.window.get_screen()
        self.provider.load_from_path("../glade/style.css")
        self.style = self.window.get_style_context()
        self.style.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.lines = 27
        self.c = self.builder.get_object("LineContainer")
        self.line = self.builder.get_object("Line0")
        self.line.connect("key-press-event", self.moveNext)
        self.line.connect("key-press-event", self.movePrevious)

        editor = self.builderEd.get_object("editor")
        #editor.show()

        for l in range(self.lines):


            if l >= 29:
                #print("NUMBER",str(l))
                c = self.builder.get_object("Line"+str(l))
                c.connect("key-press-event", self.moveNext)
                c.connect("key-press-event", self.movePrevious)
                b = self.builder.get_object("button-"+str(l))
                b.connect("button-press-event", self.addBar)
                lab = self.builder.get_object(str(l))
                if l == 28 or l == 29:
                    print("donothing")
                else:
                    lab.set_text("   ")
                    #uncomment the below line for line numbers
                    #lab.set_text(str(l-29))
                    

                    lab.show()
            else:
                c = self.builder.get_object("Line"+str(l))
                c.connect("key-press-event", self.moveNext)
                c.connect("key-press-event", self.movePrevious)
                lab = self.builder.get_object(str(l))
                b = self.builder.get_object("button-"+str(l))
                b.connect("button-press-event", self.addBar)
                lab.set_text("   ")
                #uncomment the below line for line numbers
                #lab.set_text(str(l))
                lab.show()
        
        output = ""
        l = ""
        for i in range(self.lines):
            if i < self.lines:
                file = open("../templates/atLine", "r")
                l += file.readline()
                file.close()
                self.lineContent.append(l)
                output += l + str("\n")
        self.c.add(self.line)
        self.c.show()
        
        self.window.connect("destroy", Gtk.main_quit)
        self.window.set_title("Hexagon Discourse")

        #self.window.show_all()
        for i in range(self.lines):
            end = self.spawn()
            if end :
                return
            self.c.show()
            self.window.show_all()
            time.sleep(0.01)
        print(len(self.lineContent))
    #
    def addBar(self, button, event):
        for i in range(27):
            pos = self.builder.get_object("Line"+str(i))

            if pos.is_focus():
                print("Attaching a descendent node.")
                bar = Gtk.Entry()
                s = bar.get_style_context()
                s.add_class("GtkEntry")
                s.add_class("levelOne")
                bar.show()
                if i > 27:
                    box = self.builder.get_object("Box"+str(i-2))
                else:
                    box = self.builder.get_object("Box"+str(i+1))
                box.add(bar)
                box.show_all()
    def moveNext(self, key, event):
        print("HIT A KEY")
        print(key)
        allnames = []
        for i in range(27):
            allnames.append("Line"+str(i))
        
        keyname = Gdk.keyval_name(event.keyval)
        print(keyname)
        count = 0
        keyname = keyname.translate(str.maketrans('', '', ' \n\t\r'))
        if keyname == 'Return' or keyname == 'KP_Enter':
            for n in allnames:
                if count >= len(allnames):
                    count = 0
                
                line = self.builder.get_object(n)
                print(str(n[:4]+str(count)))
                #I hate hardcoding, but will work for now
                if line.is_focus():
                    newLine = self.builder.get_object(n[:4]+str(count+1))
                    newLine.grab_focus()
                    newLine.show()
                    return
                count += 1
    def movePrevious(self, key, event):
        print("HIT A KEY")
        print(key)
        allnames = []
        for i in range(26):
            allnames.append("Line"+str(i))
        
        keyname = Gdk.keyval_name(event.keyval)
        print(keyname)
        count = 0
        keyname = keyname.translate(str.maketrans('', '', ' \n\t\r'))
        if keyname == 'Up':
            for n in allnames:
                if count >= len(allnames):
                    count = 0
                
                line = self.builder.get_object(n)
                print(str(n[:4]+str(count)))
                #I hate hardcoding, but will work for now
                if line.is_focus():
                    newLine = self.builder.get_object(n[:4]+str(count-1))
                    newLine.grab_focus()
                    newLine.show()
                    return
                count += 1
   
    def spawn(self):
        if self.lineCount >= 27:
            print(len(self.lineContent))
            return True

        added = Gtk.Entry()
        added.style = added.get_style_context()
        added.style.add_class("GtkEntry")
        #print("NEW NAME"+str(self.lineCount))
        added.set_name(str(self.lineCount))
        self.LineNames.append(added.get_name())
        line = self.builder.get_object("Line0")
        added.connect("key-press-event", self.moveNext)
        added.connect("key-press-event", self.movePrevious)
        #added.set_text(line.get_text())
        #self.c.add(added)
        #self.Lines.append(added)
        #self.c.show()
        
        self.lineCount += 1
        #self.window.show_all()
        return False
    def main(self):
        Gtk.main()
win = Window()
win.main()
