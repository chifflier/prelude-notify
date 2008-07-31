import time
import gobject
import pynotify

class HeartbeatSource:
        def _update_fields(self, idmef):
                self._heartbeat_interval = idmef.Get("heartbeat.heartbeat_interval")
                self._last = time.time()

                self._name = idmef.Get("heartbeat.analyzer(-1).name")
                self._model = idmef.Get("heartbeat.analyzer(-1).model")
                self._analyzerid = idmef.Get("heartbeat.analyzer(-1).analyzerid")
                self._node_name = idmef.Get("heartbeat.analyzer(-1).node.name")
                self._node_location = idmef.Get("heartbeat.analyzer(-1).node.location")
                self._node_addresses = idmef.Get("heartbeat.analyzer(-1).node.address(*).address")


        def __init__(self, env, idmef):
                self._env = env
                self._delta = 3
                self._timer = None
                self._is_dead = False
                self.update(idmef)

        def _genid(self):
                str = ""

                if self._name:
                        str += self._name
                        if self._model:
                                str += " (%s)" % self._model
                elif self._model:
                        str += self._model

                elif self._analyzerid:
                        str += self._analyzerid

                str += " on "
                if self._node_name:
                        str += self._node_name
                        if self._node_location:
                                str += ", " + self._node_location
                return str

        def _heartbeat_timer_cb(self):
                self._is_dead = True

                self._env.notify.run("high", None, "Missing agent",
                                     "No heartbeat received for %s" % self._genid(), aggregate=False)
                return False

        def update(self, idmef):
                if self._is_dead:
                        self._is_dead = False
                        self._env.notify.run(None, None, "Agent back online",
                                             "Missing analyzer %s is back online" % self._genid(), aggregate=False)

                if self._timer:
                        gobject.source_remove(self._timer)

                self._update_fields(idmef)

                if not self._is_dead:
                        self._timer = gobject.timeout_add((self._heartbeat_interval + self._delta) * 1000, self._heartbeat_timer_cb)


class HeartbeatMonitor:
        def __init__(self, env):
                self._env = env
                self._table = {}

        def heartbeat(self, idmef):
            analyzerid = idmef.Get("heartbeat.analyzer(-1).analyzerid")

            if self._table.has_key(analyzerid):
                self._table[analyzerid].update(idmef)
            else:
                self._table[analyzerid] = HeartbeatSource(self._env, idmef)
