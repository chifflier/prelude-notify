#!/usr/bin/env python

import PreludeEasy
from PreludeEasy import ConnectionPool, Connection
import gobject, gtk

import notifyaction
import pnconfig


Notify = notifyaction.PreludeNotify()

c = PreludeEasy.ClientEasy("prelude-notify", PreludeEasy.Client.IDMEF_READ)
c.SetFlags(PreludeEasy.Client.CONNECT)
pool = c.GetConnectionPool()
pool.AddConnection(Connection("127.0.0.1"))

c.Start()

def PollIDMEF():
	idmef = PreludeEasy.IDMEF()
	ret = c.RecvIDMEF(idmef, 100)
	if ret:
		Notify.run(idmef.Get("alert.source(0).node.address(0).address") or "(unknown)",
				idmef.Get("alert.classification.text"))
	return 1

#print pnconfig.iconok
icon = gtk.status_icon_new_from_file(pnconfig.iconok)
gobject.idle_add(PollIDMEF)
gtk.main()

