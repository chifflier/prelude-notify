#!/usr/bin/env python

import PreludeEasy
from PreludeEasy import ConnectionPool, Connection
import threading
import gtk

import notifyaction
import pnconfig

gtk.gdk.threads_init()


Notify = notifyaction.PreludeNotify()

class PreludeEventReader(threading.Thread):
        c = PreludeEasy.ClientEasy("prelude-notify", PreludeEasy.Client.IDMEF_READ)
        stopthread = threading.Event()
        def __init__(self, addr):
                threading.Thread.__init__(self)
                self.c.SetFlags(PreludeEasy.Client.CONNECT)
                pool = self.c.GetConnectionPool()
                pool.AddConnection(Connection(addr))

        def run(self):
                self.c.Start()
                while not self.stopthread.isSet():
                        idmef = PreludeEasy.IDMEF()
                        ret = self.c.RecvIDMEF(idmef)
                        Notify.run(idmef.Get("alert.source(0).node.address(0).address") or "(unknown)",
                                        idmef.Get("alert.classification.text"))

        def stop(self):
                self.stopthread.set()


per = PreludeEventReader("192.168.0.10")
per.start()

print pnconfig.iconok
icon = gtk.status_icon_new_from_file(pnconfig.iconok)
gtk.main()

