#!/usr/bin/env python

import PreludeEasy
from PreludeEasy import ConnectionPool, Connection
import pynotify

pynotify.init("PreludeNotify")

c = PreludeEasy.ClientEasy("prelude-notify", PreludeEasy.Client.IDMEF_READ)
c.SetFlags(PreludeEasy.Client.CONNECT)
pool = c.GetConnectionPool()
pool.AddConnection(Connection("192.168.0.10"))

c.Start()

while True:
    idmef = PreludeEasy.IDMEF()
    ret = c.RecvIDMEF(idmef)
    n = pynotify.Notification(idmef.Get("alert.source(0).node.address(0).address") or "(unknown)",
                              idmef.Get("alert.classification.text"))
    n.show()

