import gobject

class ThresholdItem:
    pass

class Threshold:
    def __init__(self, threshold_timeout, expire_cb):
        self._limited = { }
        self._timeout = int(threshold_timeout) * 1000
        self._expire_cb = expire_cb
        self._limit_path = [ "alert.source(*).node.address(*).address", "alert.classification.text" ]

    def _timer_cb(self, item):
        self._limited.pop(item.key)
        self._expire_cb(item)
        return False

    def _setTimer(self, item):
        item.timer = gobject.timeout_add(self._timeout, self._timer_cb, item)

    def _newEntry(self, key, idmef):
        item = self._limited[key] = ThresholdItem()
        item.key = key
        item.count = 1
        item.idmef = idmef
        item.messageid = [ idmef.Get("alert.messageid") ]
        self._setTimer(item)

    def _updateEntry(self, key, idmef):
        item = self._limited[key]
        item.count = item.count + 1
        item.messageid.append(idmef.Get("alert.messageid"))

        gobject.source_remove(item.timer)
        self._setTimer(item)

    def thresholdMessage(self, idmef):
        rl = []

        for i in self._limit_path:
            rl += [idmef.Get(i)]

        key = str(rl)
        if self._limited.has_key(key):
            self._updateEntry(key, idmef)
        else:
            self._newEntry(key, idmef)
