#!/usr/bin/env python

import PreludeEasy
from PreludeEasy import ConnectionPool, Connection
import gobject, gtk

import notifyaction
import pnstatusicon
import pnconfig, threshold

Notify = notifyaction.PreludeNotify()

def _expire_cb(item):
    idmef = item.idmef

    if item.count > 1:
        cstr = "%d x " % item.count
    else:
        cstr = ""

    Notify.run(cstr + (idmef.Get("alert.source(0).node.address(0).address") or "(unknown)"),
               idmef.Get("alert.classification.text"))


thresholding = threshold.Threshold(_expire_cb)

config = pnconfig.PnConfig()

c = PreludeEasy.ClientEasy("prelude-notify", PreludeEasy.Client.IDMEF_READ)
c.SetFlags(PreludeEasy.Client.CONNECT)
pool = c.GetConnectionPool()
manager_addresses = config.get("manager", "addresses").split(',')
for addr in manager_addresses:
	pool.AddConnection(Connection(addr))

c.Start()

def PollIDMEF():
        idmef = PreludeEasy.IDMEF()

        ret = c.RecvIDMEF(idmef, 100)
        if ret:
                thresholding.thresholdMessage(idmef)

        return 1

statusicon = pnstatusicon.PreludeStatusIcon()
gobject.idle_add(PollIDMEF)
gtk.main()

