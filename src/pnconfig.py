import os
from ConfigParser import SafeConfigParser

iconok = "../pixmaps/tray/brouette-ok-icon.png"
themespath = "../pixmaps/themes/"

class PnConfig():
	cp = SafeConfigParser()
	def __init__(self):
		configname = "%s/.prelude-notify.rc" % os.getenv("HOME")
		if not os.path.exists(configname):
			# Write the default configuration file
			FILE = open(configname,"w")
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
		else:
			self.cp.read(configname)

	def get(self, section, key):
		return self.cp.get(section, key)
