# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoann.v@prelude-ids.com>
#
# This file is part of the Prewikka program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

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
                self._timeout = None
                self.doConnect()

        def __del__(self):
                self.close()

        def close(self):
                if self._iow:
                        gobject.source_remove(self._iow)
                        self._iow = None

                if self._timeout:
                        gobject.source_remove(self._timeout)
                        self._timeout = None


        def _io_cb(self, fd, cond, con):
                if cond & gobject.IO_IN:
                        try:
                                idmef = con.RecvIDMEF()
                        except PreludeError, err:
                                self.handleDisconnect(con, str(err))
                                return False

                        if idmef.Get("heartbeat.create_time"):
                                self.env.hbmonitor.heartbeat(idmef)

                        elif self.env.criteria is None or self.env.criteria.Match(idmef):
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

                return False

        def handleDisconnect(self, err=""):
                if err:
                        err = ": " + err
                self.env.notify.run("high", None, "Manager Connection interrupted", "With Prelude-Manager <b>%s</b>%s" % (self._con.GetPeerAddr(), err))
                self._timeout = gobject.timeout_add(10000, self.doConnect)


class Session:
        def __init__(self, env, profile):
                self.env = env
                self.client = PreludeEasy.ClientEasy(profile, PreludeEasy.Client.IDMEF_READ)
                self.client.SetFlags(0)
                self._con_list = {}

        def addAddress(self, addr):
                self._con_list[addr] = SingleConnection(self.env, self.client, addr)

        def delAddress(self, addr):
                self._con_list[addr].close()
                self._con_list.pop(addr)

        def close(self):
                for i in self._con_list.keys():
                        self._con_list[i].close()
