import gobject
import pynotify
import webbrowser
import urllib

import pnconfig

class PreludeNotify:
        def __init__(self, config):
                pynotify.init("PreludeNotify")
                self.loop = gobject.MainLoop()
                self.conf = config

        def _prewikka_view_cb(self, n, action, data):
                if len(data) > 1:
                        j = 0
                        mid = ""
                        for id in data:
                                operator = urllib.quote("=")
                                mid += "&classification_object_%d=alert.messageid&classification_operator_%d=%s&classification_value_%d=%s" % (j, j, operator, j, urllib.quote(id))
                                j += 1

                        url = "%s?view=alert_listing%s" % (self.conf.get("prewikka", "url"), mid)
                else:
                        url = "%s?view=alert_summary&origin=alert_listing&messageid=%s" % (self.conf.get("prewikka", "url"), data[0])

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
