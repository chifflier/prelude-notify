# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Sebastien Tricaud <toady@inl.fr>
#
# This file is part of the Prewikka program.
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

try:
        import ctypes, ctypes.util

        class XScreenSaverInfo(ctypes.Structure):
                """ typedef struct { ... } XScreenSaverInfo; """
                _fields_ = [('window',      ctypes.c_ulong), # screen saver window
                    ('state',       ctypes.c_int),   # off,on,disabled
                    ('kind',        ctypes.c_int),   # blanked,internal,external
                    ('since',       ctypes.c_ulong), # milliseconds
                    ('idle',        ctypes.c_ulong), # milliseconds
                    ('event_mask',  ctypes.c_ulong)] # events

        have_ctype = True
except ImportError:
        have_ctype = False

import os
import time

class X11Idle:
        def __init__(self):
                self.xss = None

                if not have_ctype:
                        return

                try:
                        xlib = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11"))
                except:
                        print "X11 library not found"
                        return

                self.dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
                self.root = xlib.XDefaultRootWindow(self.dpy)
                try:
                        self.xss = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Xss"))
                except:
                        print "XSS unsupported"
                        return

                self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
                self.xss_info = self.xss.XScreenSaverAllocInfo()

        def IdleTimeGet(self):
                if not self.xss:
                        return 0

                self.xss.XScreenSaverQueryInfo(self.dpy, self.root, self.xss_info)

                return self.xss_info.contents.idle / 1000


if __name__ == "__main__":
        idle = X11Idle()
        while 1:
                print str(idle.IdleTimeGet())
                time.sleep(1)

