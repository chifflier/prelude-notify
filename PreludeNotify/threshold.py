# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoann.v@prelude-ids.com>
#
# This file is part of the Prelude-Notify program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

import gobject

class ThresholdItem:
    pass

class Threshold:
    def __init__(self, threshold_timeout, expire_cb):
        self._limited = { }
        self._expire_cb = expire_cb
        self._limit_path = [ "alert.source(*).node.address(*).address", "alert.classification.text" ]
        self.setExpire(threshold_timeout)

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

    def setExpire(self, threshold_timeout):
        self._timeout = int(threshold_timeout) * 1000

    def thresholdMessage(self, idmef):
        rl = []

        for i in self._limit_path:
            rl += [idmef.Get(i)]

        key = str(rl)
        if self._limited.has_key(key):
            self._updateEntry(key, idmef)
        else:
            self._newEntry(key, idmef)
