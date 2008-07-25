import gobject
import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")
                self.loop = gobject.MainLoop()

        def _prewikka_view_cb(self, n, action, data):
                url = "%s?view=alert_summary&origin=alert_listing&messageid=%s" % ("https://demo.prelude-ids.com/", data)

                print "Open URL: " + url

                n.close()
                self.loop.quit()

        def run(self, imageuri, messageid, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                n.add_action("pview", "Prewikka View", self._prewikka_view_cb, messageid)
                n.show()

                self.loop.run()
