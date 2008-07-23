import os
from PreludeNotify import siteconfig
from ConfigParser import SafeConfigParser

iconok = siteconfig.prefix + "/share/prelude-notify/tray/brouette-ok-icon.png"
themespath = siteconfig.prefix + "/share/prelude-notify/themes/"

class PnConfig():
	cp = SafeConfigParser()
	configname = ""
	def __init__(self):
		self.configname = "%s/.prelude-notifyrc" % os.getenv("HOME")
		if not os.path.exists(self.configname):
			# Write the default configuration file
			FILE = open(self.configname,"w")
			FILE.write("[idmef]\n")
			FILE.write("profile=prelude-notify\n")
			FILE.write("filter=\n\n")
			FILE.write("[manager]\n")
			FILE.write("addresses=127.0.0.1\n\n")
			FILE.write("[prewikka]\n")
			FILE.write("url=http://localhost:8000\n\n")
			FILE.write("[ui]\n")
			FILE.write("theme=default\n")
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
