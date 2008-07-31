import gobject
import pynotify
import webbrowser
import urllib
import pnconfig
import time


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


class NotifyNow:
        def __init__(self, env):
                pynotify.init("PreludeNotify")
                self._env = env
                self._pynotify_bug = [ ]

        def _handle_closed(self, n):
                self._pynotify_bug.remove(n)

        def _prewikka_view_cb(self, n, action, messageid):
                self._pynotify_bug.remove(n)

                if self._env.config.get("ui", "browser") == "auto":
                        webbrowser.open(PrewikkaURL(self._env.config, messageid), autoraise=True)

                n.close()

        def run(self, imageuri, messageid, urgency, title, message):
                n = pynotify.Notification(title, message, imageuri)

                if urgency is not None:
                    n.set_urgency(urgency)

                if messageid and self._env.config.get("prewikka", "url"):
                        n.data = messageid
                        self._pynotify_bug.append(n)

                        n.add_action("response", "Prewikka View", self._prewikka_view_cb, messageid)
                        n.connect("closed", self._handle_closed)

                n.show()

class QueuedNotification:
        def __init__(self, *args):
                self._time = time.time()
                self._args = args

class NotifyQueue(NotifyNow):
        def __init__(self, env):
                NotifyNow.__init__(self, env)
                self._ag_queue = []
                self._no_ag_queue = []
                self._count = 0

        def flush(self):
                if self._count == 0:
                        return

                end = time.time()

                for i in self._no_ag_queue:
                        args = i._args
                        NotifyNow.run(self, *args)

                NotifyNow.run(self, None, self._ag_queue, None,
                              "Events received while idle",
                              "%d events received while you were away for %d seconds" % (self._count, end - self._time))

                self._count = 0
                self._ag_queue = []
                self._no_ag_queue = []

        def run(self, *args, **kwargs):
                if self._count == 0:
                        self._time = time.time()

                print kwargs.keys()

                self._count += 1
                if kwargs["aggregate"]:
                        self._ag_queue.append(args[1])
                else:
                        self._no_ag_queue.append(QueuedNotification(*args))


class PreludeNotify(NotifyQueue, NotifyNow):
        def __init__(self, env):
                NotifyQueue.__init__(self, env)

        def run(self, imageuri, messageid, urgency, title, message, aggregate=True):
                if not self._env.is_idle:
                        NotifyNow.run(self, imageuri, messageid, urgency, title, message)
                else:
                        NotifyQueue.run(self, imageuri, messageid, urgency, title, message, aggregate=aggregate)
