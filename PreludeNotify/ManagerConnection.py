from PreludeEasy import ClientEasy, Connection, PreludeError
from PreludeNotify import ErrorDialog

import gobject
import os

class Session:
        _addrevents = {}

        def __init__(self, env, hbmonitor):
                self.con = None
                self.env = env
                self.hbmonitor = hbmonitor

        def doConnect(self):
                try:
                        self.con.Connect(self.env.client, ClientEasy.IDMEF_READ)

                #except PreludeError.PROFILE:
                #        ErrorDialog.CreateProfile(c, ClientEasy.IDMEF_READ, env.config.get("idmef", "profile"))
                #        return False

                except PreludeError, err:
                        ErrorDialog.ErrorDialog(str(err))
                        return True

                self.env.notify.run(None, None, "Manager Connection successfull", "With Prelude-Manager <b>%s</b>" % self.con.GetPeerAddr())

        def handleDisconnect(self, err=""):
                if err:
                        err = ": " + err
                self.env.notify.run("high", None, "Manager Connection interrupted", "With Prelude-Manager <b>%s</b>%s" % (self.con.GetPeerAddr(), err))
                gobject.timeout_add(10000, self.doConnect)

        def ConnectAddresses(self, manager_addresses):
                manager_addresses = manager_addresses.split(',')
                for addr in manager_addresses:
                        self.con = Connection(addr)
                        self.doConnect()
                        self._addrevents[addr] = gobject.io_add_watch(self.con.GetFd(), gobject.IO_IN|gobject.IO_PRI|gobject.IO_HUP|gobject.IO_NVAL|gobject.IO_ERR, self.io_cb, self.con)

        def delCon(self):
                for addr in self._addrevents:
                        gobject.source_remove(self._addrevents[addr])

        def io_cb(self, fd, cond, con):
                if cond & gobject.IO_IN:
                        try:
                                idmef = con.RecvIDMEF()
                        except PreludeError, err:
                                self.handleDisconnect(con, str(err))
                                return False

                        if idmef.Get("heartbeat.create_time"):
                                self.hbmonitor.heartbeat(idmef)

                        elif (not self.env.criteria) or (self.env.criteria.match(idmef)):
                                self.env.thresholding.thresholdMessage(idmef)

                if cond & gobject.IO_ERR or cond & gobject.IO_HUP:
                        self.handleDisconnect(con)
                        return False

                return True

