import os
from PreludeNotify import siteconfig
from ConfigParser import SafeConfigParser

iconok = siteconfig.prefix + "/share/prelude-notify/tray/notify-ok.png"
iconbad = siteconfig.prefix + "/share/prelude-notify/tray/notify-bad.png"
themespath = siteconfig.prefix + "/share/prelude-notify/themes/"

class PnConfig:
	cp = SafeConfigParser()
	configname = ""
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
		self.cp.set(section, key, value)
		FILE = open(self.configname,"w")
		self.cp.write(FILE)
		FILE.close()

