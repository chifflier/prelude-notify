import gobject
import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")
		self.loop = gobject.MainLoop()

        def _prewikka_view_cb(self, n, action, data):
		url = "<a href=\"localhost/?view=alert_summary&messageid=" + data + "\">\n"

		print "Open URL: " + url

	        notification.close()
                gobject.MainLoop().quit(self.loop)

        def run(self, imageuri, messageid, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                n.add_action("pview", "Prewikka View", self._prewikka_view_cb, messageid)
                n.show()

            	gobject.MainLoop().run(self.loop)

