import os
import PreludeEasy

import ErrorDialog

from PreludeNotify import siteconfig
from ConfigParser import SafeConfigParser

iconok = siteconfig.prefix + "/share/prelude-notify/tray/notify-ok.png"
iconbad = siteconfig.prefix + "/share/prelude-notify/tray/notify-bad.png"
themespath = siteconfig.prefix + "/share/prelude-notify/themes/"

class PnConfig:
	cp = SafeConfigParser()
	configname = ""
	_configtable = {} # configtable['manager_addresses'] = ['oldvalues', 'newvalues']
	def __init__(self):
		self.configname = "%s/.prelude-notifyrc" % os.getenv("HOME")
		if not os.path.exists(self.configname):
			# Write the default configuration file
			FILE = open(self.configname,"w")
			FILE.write("[general]\n")
			FILE.write("# Time in seconds for alert grouping\n")
			FILE.write("threshold_timeout=5\n")
			FILE.write("# Time in seconds before thinking you are away from keyboard and missing alerts\n")
			FILE.write("X11idle_timeout=5\n")
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

		self.cp.set(section, key, value)
		FILE = open(self.configname,"w")
		self.cp.write(FILE)
		FILE.close()

	def update(self):
		for section_key in self._configtable:
			if section_key == "idmef_profile":
				old = self._configtable[section_key][0]
				new = self._configtable[section_key][1]
				if old != new:
					manager_addr = self._configtable["manager_addresses"][1]
					self.client = None
					self.client = PreludeEasy.ClientEasy(new, PreludeEasy.Client.IDMEF_READ)
					self.client.SetFlags(0)
					try:
						self.client.Start()
					except:
						ErrorDialog.CreateProfile(new, manager_addr)

					self.managercon.delCon()
					self.managercon.ConnectAddresses(manager_addr)

			if section_key == "manager_addresses":
				old = self._configtable[section_key][0]
				new = self._configtable[section_key][1]
				if old != new:
					self.managercon.delCon()
					self.managercon.ConnectAddresses(new)


