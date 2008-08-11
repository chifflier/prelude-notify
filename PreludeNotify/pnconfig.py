import os
import PreludeEasy
import ErrorDialog
from ManagerConnection import Session
from PreludeNotify import siteconfig
from ConfigParser import SafeConfigParser

iconok = siteconfig.prefix + "/share/prelude-notify/tray/notify-ok.png"
iconbad = siteconfig.prefix + "/share/prelude-notify/tray/notify-bad.png"
themespath = siteconfig.prefix + "/share/prelude-notify/themes/"

class PnConfig:
        cp = SafeConfigParser()
        configname = ""
        _configtable = {} # configtable['manager_addresses'] = ['oldvalues', 'newvalues']
        def __init__(self, env):
                self.env = env
                self.configname = "%s/.prelude-notifyrc" % os.getenv("HOME")
                if not os.path.exists(self.configname):
                        # Write the default configuration file
                        FILE = open(self.configname,"w")
                        FILE.write("[general]\n")
                        FILE.write("# Time in seconds for alert grouping\n")
                        FILE.write("threshold_timeout=5\n")
                        FILE.write("# Time in seconds before thinking you are away from keyboard and missing alerts\n")
                        FILE.write("x11idle_timeout=5\n")
                        FILE.write("[idmef]\n")
                        FILE.write("profile=prelude-notify\n")
                        FILE.write("filter=\n\n")
                        FILE.write("[manager]\n")
                        FILE.write("addresses=127.0.0.1\n\n")
                        FILE.write("[prewikka]\n")
                        FILE.write("url=http://localhost:8000\n\n")
                        FILE.write("[ui]\n")
                        FILE.write("theme=default\n")
                        FILE.write("browser=auto\n")
                        FILE.close()
                        self.cp.read(self.configname)
                else:
                        self.cp.read(self.configname)

        def get(self, section, key):
                return self.cp.get(section, key)

        def set(self, section, key, value):
                # We create a config table to watch what changed
                # and update accordingly
                section_key = "%s_%s" % (section, key)
                self._configtable[section_key] = []
                self._configtable[section_key].append(self.get(section, key))
                self._configtable[section_key].append(value)


        def update(self):
                for section_key in self._configtable:
                        if section_key == "idmef_profile":
                                old = self._configtable[section_key][0]
                                new = self._configtable[section_key][1]
                                if old != new:
                                        manager_addr = self._configtable["manager_addresses"][1]
                                        self.env.managercon = Session(self.env, new)
                                        for addr in manager_addr.split(","):
                                                self.env.managercon.addAddress(addr)


                        if section_key == "manager_addresses":
                                old = self._configtable[section_key][0]
                                new = self._configtable[section_key][1]
                                if old != new:
                                        self.env.managercon.delAddress(old)
                                        self.env.managercon.addAddress(new)


