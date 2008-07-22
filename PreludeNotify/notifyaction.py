import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")

        def _view_cb(self, notification, action, data=None):
            print "view_cb"
            notification.close()

        def _prewikka_view_cb(self, notification, action, data=None):
            print "prewikka_view_cb"
            notification.close()

        def run(self, imageuri, title, message):
                n = pynotify.Notification(title, message, imageuri)
                n.add_action("clicked", "View", self._view_cb, None)
                n.add_action("clicked", "Prewikka View", self._prewikka_view_cb, None)
                n.show()

