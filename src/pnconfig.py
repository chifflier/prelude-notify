import os
from ConfigParser import SafeConfigParser

iconok = "../pixmaps/tray/brouette-ok-icon.png"

class PnConfig():
	def __init__(self):
		configname = "%s/.prelude-notify.rc" % os.getenv("HOME")
		if not os.path.exists(configname):
			# Write the default configuration file
			FILE = open(configname,"w")
			FILE.write("[idmef]\n")
			FILE.write("profile=prelude-notify\n")
			FILE.write("filter=\n\n")
			FILE.write("[manager]\n")
			FILE.write("addresses=\n\n")
			FILE.write("[prewikka]\n")
			FILE.write("url=\n\n")
			FILE.write("[ui]\n")
			FILE.write("theme=default\n")
			FILE.close()
		else:
			cp = SafeConfigParser()
			cp.read(configname)

	def get(self, section, key):
		return self.cp.get(section, key)
