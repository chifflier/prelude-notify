from PreludeEasy import ClientEasy, Connection, PreludeError
from PreludeNotify import ErrorDialog

import PreludeEasy
import gobject
import os


class SingleConnection:
        def __init__(self, env, client, addr):
                self.env = env
                self._client = client
                self._con = Connection(addr)
                self._iow = None
                self.doConnect()

        def __del__(self):
                if self._iow:
                        gobject.source_remove(self._iow)

        def _io_cb(self, fd, cond, con):
                if cond & gobject.IO_IN:
                        try:
                                idmef = con.RecvIDMEF()
                        except PreludeError, err:
                                self.handleDisconnect(con, str(err))
                                return False

                        if idmef.Get("heartbeat.create_time"):
                                self.env.hbmonitor.heartbeat(idmef)

                        elif (not self.env.criteria) or (self.env.criteria.match(idmef)):
                                self.env.thresholding.thresholdMessage(idmef)

                if cond & gobject.IO_ERR or cond & gobject.IO_HUP:
                        self.handleDisconnect(con)
                        return False

                return True

        def doConnect(self):
                try:
                        self._con.Connect(self._client, ClientEasy.IDMEF_READ)

                except PreludeError, err:
                        ErrorDialog.ErrorDialog(str(err))
                        return True

                self._iow = gobject.io_add_watch(self._con.GetFd(), gobject.IO_IN|gobject.IO_PRI|gobject.IO_HUP|gobject.IO_NVAL|gobject.IO_ERR, self._io_cb, self._con)
                self.env.notify.run(None, None, "Manager Connection successfull", "With Prelude-Manager <b>%s</b>" % self._con.GetPeerAddr())

        def handleDisconnect(self, err=""):
                if err:
                        err = ": " + err
                self.env.notify.run("high", None, "Manager Connection interrupted", "With Prelude-Manager <b>%s</b>%s" % (self._con.GetPeerAddr(), err))
                gobject.timeout_add(10000, self.doConnect)


class Session:
        _addrevents = {}

        def __init__(self, env, profile):
                print "Create client session"
                self.env = env
                self.client = PreludeEasy.ClientEasy(profile, PreludeEasy.Client.IDMEF_READ)
                self.client.SetFlags(0)
                self._con_list = {}

        def addAddress(self, addr):
                self._con_list[addr] = SingleConnection(self.env, self.client, addr)

        def delAddress(self, addr):
                del(self._con_list[addr])
