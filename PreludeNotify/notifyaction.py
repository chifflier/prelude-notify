import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")

        def _view_cb(self, n, action):
            print action
            print "view_cb"
            notification.close()

        def _prewikka_view_cb(self, n, action):
            print "prewikka_view_cb"
            notification.close()

        def run(self, imageuri, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                n.add_action("view", "View", self._view_cb)
                n.add_action("pview", "Prewikka View", self._prewikka_view_cb)
                n.show()

