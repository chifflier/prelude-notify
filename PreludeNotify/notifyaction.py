import gobject
import pynotify

import webbrowser

import pnconfig

class PreludeNotify:
        def __init__(self, config):
                pynotify.init("PreludeNotify")
                self.loop = gobject.MainLoop()
		self.conf = config

        def _prewikka_view_cb(self, n, action, data):
                url = "%s?view=alert_summary&origin=alert_listing&messageid=%s" % (self.conf.get("prewikka", "url"), data)

                #print "Open URL: " + url
		if self.conf.get("ui", "browser") == "auto":
			webbrowser.open(url)

                n.close()
                self.loop.quit()

        def run(self, imageuri, messageid, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                n.add_action("pview", "Prewikka View", self._prewikka_view_cb, messageid)
                n.show()

                self.loop.run()
