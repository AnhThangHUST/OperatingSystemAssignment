#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GObject, GLib
from task import *
import psutil
import time 
from subprocess import Popen, PIPE

class Handler:
    def __init__(self):
        self.task = Task()
    
    def gListButton_clicked_cb(self, gListButton):
        self.task.table.clear_rows()
        self.task.ListAllProcess()
        gltv_tb.set_text(self.task.table.get_string())	

    def gExhaustMemoryButton_clicked_cb(self, gExhaustMemoryButton):
        self.task.table.clear_rows()
        self.task.ListAllProcess()
        priorities = dict()
        for i in range (len(gkp)):
            if gkp[i].get_text() == "":
                continue
            priorities[gkl[i].get_text()] = int(gkp[i].get_text())
        print (priorities)
        #p = Popen(['./OOM'], shell=True, stdout=PIPE, stdin=PIPE)
        #if psutil.virtual_memory().percent > 90:
        self.task.KillBasedOnPriority(priorities)

def MemoryInfoRealTime():
    while (1):
        GLib.idle_add(info)
        time.sleep(1)
    
def info():
    sizeOfRam = psutil.virtual_memory().total /2**30
    RamUsage = psutil.virtual_memory().percent
    sizeOfSwap = psutil.swap_memory().total /2**30
    gstb.set_text(str(round(sizeOfSwap,2)))
    gmtb.set_text(str(round(sizeOfRam,2)))
    gpmtb.set_text(str(RamUsage))

gb = Gtk.Builder()
gb.add_from_file("gp008_Thang.glade")
gb.connect_signals(Handler())
gw = gb.get_object("gWindow")
glb = gb.get_object("gListButton")
gkb = gb.get_object("gKillButton")

pfd = Pango.FontDescription("Courier 11")

gltv = gb.get_object("gListTextView")
gltv.modify_font(pfd)
gltv_tb = gltv.get_buffer()
gkp = [] # mang priority cua cac process
gkl = [] # mang chua cac ten process can kill
for i in range(5):
    gkp.append(gb.get_object("gKillPriority"+str(i)))
    gkl.append(gb.get_object("gKillLabel" +str(i)))  
gmtv = gb.get_object("gMemoryTextView")
gmtb = gmtv.get_buffer()

gstv = gb.get_object("gSwapTextView")
gstb = gstv.get_buffer()

gpmtv = gb.get_object("gPercentageMemoryTextView")
gpmtb = gpmtv.get_buffer()

gemb = gb.get_object("gExhaustMemoryButton")

gntv = gb.get_object("gNoteTextView")
GObject.threads_init()

thread  = Thread(target=MemoryInfoRealTime, args = ())
thread.start()

gw.connect("destroy", Gtk.main_quit)
gw.show_all()

Gtk.main()
