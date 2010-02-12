# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Sebastien Tricaud <toady@inl.fr>
#         Alexandre De Dommelin <adedommelin@tuxz.net>
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

import os
import PreludeEasy
import ErrorDialog
from ManagerConnection import Session
from PreludeNotify import siteconfig
from ConfigParser import SafeConfigParser

userconfigpath = "%s/.prelude-notify" % (os.getenv("HOME"))
globalthemespath = siteconfig.prefix + "/share/prelude-notify/themes"
userthemespath = userconfigpath + "/themes"

class PnConfig(SafeConfigParser):
        _globalconfigfile = siteconfig.conf_dir + "/prelude-notify.conf"
        _userconfigfile = userconfigpath + "/prelude-notifyrc"

        def __init__(self, env):
                SafeConfigParser.__init__(self)
                self._updated = {}
                self.env = env

                if os.path.exists(self._userconfigfile):
                        self.read(self._userconfigfile)
                elif os.path.exists(self._globalconfigfile):
                        self.read(self._globalconfigfile)
                else:
                        SafeConfigParser.set(self, "general", "threshold_timeout", "5")
                        SafeConfigParser.set(self, "general", "x11_idle_timeout", "5")
                        SafeConfigParser.set(self, "idmef", "profile", "prelude-notify")
                        SafeConfigParser.set(self, "idmef", "filter", "")
                        SafeConfigParser.set(self, "manager", "addresses", "127.0.0.1")
                        SafeConfigParser.set(self, "prewikka", "url", "http://localhost:8000")
                        SafeConfigParser.set(self, "ui", "theme", "default")
                        SafeConfigParser.set(self, "ui", "browser", "auto")



		_configtheme = SafeConfigParser.get(self,"ui","theme")

		if os.path.isdir( userthemespath + "/" + _configtheme ):
			self.theme = userthemespath + "/" + _configtheme
		elif os.path.isdir( globalthemespath + "/" +  _configtheme ):
			self.theme = globalthemespath + "/" + _configtheme
		else:
			self.theme = globalthemespath + "/" + "default"

	def getIconOk(self):
		return self.theme + "/tray/notify-ok.png"

	def getIconBad(self):
		return self.theme + "/tray/notify-bad.png"

	def getThemePath(self):
		return self.theme

        def set(self, section, key, value):
                old = SafeConfigParser.get(self, section, key)

                if value != old:
                        self._updated[key] = section, key, value

                return SafeConfigParser.set(self, section, key, value)

        def _update(self):
                if self._updated.has_key("profile") or self._updated.has_key("addresses"):
                        self.env.managercon.close()

                        self.env.managercon = Session(self.env, self.get("idmef", "profile"))
                        for addr in self.get("manager", "addresses").split(","):
                                self.env.managercon.addAddress(addr)

                if self._updated.has_key("filter") :
                        if self._updated["filter"] != "":
                                try:
                                        self.env.criteria = PreludeEasy.IDMEFCriteria(self._updated["filter"][3])
                                except PreludeEasy.PreludeError, e:
                                        ErrorDialog.ErrorDialog(str(e))
                                        self.set(self._updated["filter"][1], self._updated["filter"][2], self._updated["filter"][0])
                                        raise
                        else:
                                self.env.criteria = None

                if self._updated.has_key("threshold_timeout"):
                        self.env.thresholding.setExpire(self._updated["threshold_timeout"][3])

        def update(self):
                try:
                        self._update()
                except:
                        self._updated = {}
                        return
                if not os.path.isdir( userconfigpath ):
			                  os.mkdir( userconfigpath )

                self.write(open(self._userconfigfile, "w"))
