import gobject

class ThresholdItem:
    pass

class Threshold:
    def __init__(self, expire_cb):
        self._limited = { }
        self._timeout = 5
        self._expire_cb = expire_cb
        self._limit_path = [ "alert.source(0).node.address(0).address", "alert.classification.text" ]

    def _timer_cb(self, item):
        self._expire_cb(item)
        self._limited.pop(item.key)
        return False

    def _newEntry(self, key, idmef):
        item = self._limited[key] = ThresholdItem()
        item.key = key
        item.count = 1
        item.idmef = idmef
        item.timer = gobject.timeout_add(self._timeout * 1000, self._timer_cb, item)

    def _updateEntry(self, key):
        item = self._limited[key]
        item.count = item.count + 1
        gobject.source_remove(item.timer)
        item.timer = gobject.timeout_add(self._timeout * 1000, self._timer_cb, item)

    def thresholdMessage(self, idmef):
        rl = []

        for i in self._limit_path:
            rl += [idmef.Get(i)]

        key = str(rl)
        if self._limited.has_key(key):
            self._updateEntry(key)
        else:
            self._newEntry(key, idmef)
