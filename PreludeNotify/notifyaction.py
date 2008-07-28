import gobject
import pynotify
import webbrowser
import urllib

import pnconfig

def PrewikkaURL(conf, idlist):
        if len(idlist) > 1:
                j = 0
                mid = ""
                for id in idlist:
                        operator = urllib.quote("=")
                        mid += "&classification_object_%d=alert.messageid&classification_operator_%d=%s&classification_value_%d=%s" % (j, j, operator, j, urllib.quote(id))
                        j += 1

                url = "%s?view=alert_listing%s" % (conf.get("prewikka", "url"), mid)
        else:
                url = "%s?view=alert_summary&origin=alert_listing&messageid=%s" % (conf.get("prewikka", "url"), idlist[0])

        return url


class PreludeNotify:
        def __init__(self, gloop, config):
                pynotify.init("PreludeNotify")
                self.gloop = gloop
                self.conf = config

        def handle_closed(self, n, recloop):
                recloop.quit()

        def _prewikka_view_cb(self, n, action, data):
                messageid, recloop = data

                if self.conf.get("ui", "browser") == "auto":
                        webbrowser.open(PrewikkaURL(self.conf, messageid), autoraise=True)

                n.close()
                recloop.quit()

        def run(self, imageuri, messageid, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                if messageid and self.conf.get("prewikka", "url"):
                        add_action = True
                else:
                        add_action = False

                if add_action:
                        recloop = gobject.MainLoop()
                        data = (messageid, recloop)
                        n.add_action("response", "Prewikka View", self._prewikka_view_cb, data)
                        n.connect('closed', self.handle_closed, recloop)

                n.show()

                if add_action:
                        recloop.run()
