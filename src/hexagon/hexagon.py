#!/bin/bash/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


import time
import threading
import sys


class Window(Gtk.Window):
    #This is actually going to be pivotal to the whole shebang
    # We need to be able to  track what row the user is clicking on
    #and which rows should be inferred. Possibly by clicking into
    #the field, but it'd be better if they just grabbed from either
    #the for looped is_focus() part and get notified of any  
    #changes
    lp = 0

    def moveFocus(self, widget, event):
        print("There might even be an event passed")
        numLines = 28
        for i in range(28):
            o = self.builder.get_object("Line"+str(i))
            if o.has_focus():
                self.lp = i

        print("Cursor position is on row"+str(self.lp))

    def spawnEditor(self):
        builder = Gtk.Builder()
        builder.add_from_file("../glade/editor.glade")
        editor = self.builder.get_object("editor")
        #editor.show()
        for l in range(self.lines):
            c = self.builder.get_object("Line"+str(l))
            
            c.connect("key-press-event", self.moveNext)
            c.connect("key-press-event", self.movePrevious)
            c.connect("focus-in-event", self.moveFocus)
            cs = c.get_style_context()
            if l != 0:
                cs.add_class("titleBar") 
                lab = self.builder.get_object(str(l))
            else:
                cs.add_class("titleBar")

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
        self.row = 0
        self.lineCount = 0
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../glade/center.glade")
        self.builderEd = Gtk.Builder()
        self.builderEd.add_from_file("../glade/editor.glade")
        self.builderEdd = Gtk.Builder()
        self.builderEdd.add_from_file("../glade/editor.glade")

        self.found = False



        self.window = self.builder.get_object("Center")
        self.provider = Gtk.CssProvider()
        self.screen = self.window.get_screen()
        self.provider.load_from_path("../glade/style.css")
        self.style = self.window.get_style_context()
        self.style.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.lines = 28
        self.c = self.builder.get_object("LineContainer")
        self.line = self.builder.get_object("Line0")
        self.line.connect("key-press-event", self.moveNext)
        self.line.connect("key-press-event", self.movePrevious)
        self.line.connect("focus-in-event", self.moveFocus)

        editor = self.builderEd.get_object("editor")
        #editor.show()

        for l in range(self.lines):


            if l >= 29:
                #print("NUMBER",str(l))
                c = self.builder.get_object("Line"+str(l))
                c.connect("key-press-event", self.moveNext)
                c.connect("key-press-event", self.movePrevious)
                c.connect("focus-in-event", self.moveFocus)
                if l == 0:
                    ll = 1
                else:
                    ll = l
                b = self.builder.get_object("button-"+str(ll))
                b.connect("button-press-event", self.addBar)
                b.connect("activate", self.resumePosition)
                b.connect("focus-in-event", self.moveFocus)
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
                c.connect("focus-in-event", self.moveFocus)
                lab = self.builder.get_object(str(l))
                b = self.builder.get_object("button-"+str(l))
                b.connect("button-press-event", self.addBar)
                b.connect("activate", self.resumePosition)
                b.connect("focus-in-event", self.moveFocus)
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
        #not this one, this is the whole window
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
    def resumePosition(self):
        p = self.builder.get_object("Line"+str(self.lp))
        #p.grab_focus()
        return
    def addBarSec(self, button, event):
        for i in range(28, 0, -1):
            self.found = False
            if i != 0:
                pos = self.builder.get_object("Line"+str(i))
            else:
                print("nothing")
                continue
            #print("POSITION"+str(i))
            if self.lp == i and pos.is_focus():
                self.found = True
            if pos.is_focus() or self.found:
                print("Attaching a secondary descendent node.")
                holder = Gtk.Box()
                label = Gtk.Button()
                l = Gtk.Button()
                b = Gtk.Button()
                b.set_label("&")
                l.set_label("*")
                label.set_label("*")
                ls = label.get_style_context()
                ls.add_class("levelTwo")
                bs = b.get_style_context()
                bs.add_class("levelThree")
                bar = Gtk.Entry()
                s = bar.get_style_context()
                
                s.add_class("mainEntry")
                s.add_class("levelOne")
                bar.set_hexpand(True)
                bar.show()
                if i != 0:
                    box = self.builder.get_object("Box"+str(self.lp))
                    holder.add(label)
                    holder.add(l)
                    holder.add(bar)
                    box.add(holder)
                    #pos.grab_focus()
                    box.show_all()
                    if self.found:
                        self.row = i
                        return
    def addBar(self, button, event):
        for i in range(28, 0, -1):
            pos = self.builder.get_object("Line"+str(i))
            if self.lp == i and pos.is_focus():
                self.found = True
            if pos.is_focus() or self.found:
                print("Attaching a descendent node.")
                holder = Gtk.Box()
                label = Gtk.Button()
                label.connect("button-press-event", self.addBarSec)
                label.connect("focus-in-event", self.moveFocus)
                label.set_label("*")
                ls = label.get_style_context()
                ls.add_class("levelTwo")
                bar = Gtk.Entry()
                s = bar.get_style_context()
                s.add_class("mainEntry")
                s.add_class("levelOne")
                bar.set_hexpand(True)
                bar.show()
                if i != 0:
                    box = self.builder.get_object("Box"+str(self.lp+1))
                    holder.add(label)
                    holder.add(bar)
                    box.add(holder)
                    #pos.grab_focus()
                    box.show_all()
                    if self.found:
                        self.row = i
                        return
    def moveNext(self, key, event):
        print("HIT A KEY")
        print(key)
        allnames = []
        for i in range(28):
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
                    self.lp = count
                    newLine = self.builder.get_object(n[:4]+str(count+1))
                    #newLine.grab_focus()
                    newLine.show()
                    return
                count += 1
    def movePrevious(self, key, event):
        print("HIT A KEY")
        print(key)
        allnames = []
        for i in range(27):
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
                    self.lp = count
                    newLine = self.builder.get_object(n[:4]+str(count-1))
                    #newLine.grab_focus()
                    newLine.show()
                    return
                count += 1
   
    def spawn(self):
        if self.lineCount >= 28:
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
        added.connect("focus-in-event", self.moveFocus)
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
