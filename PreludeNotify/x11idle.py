try:
	import ctypes, ctypes.util
	have_ctype = True
except:
	have_ctype = None

import os
import time

class XScreenSaverInfo( ctypes.Structure):
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window',      ctypes.c_ulong), # screen saver window
              ('state',       ctypes.c_int),   # off,on,disabled
              ('kind',        ctypes.c_int),   # blanked,internal,external
              ('since',       ctypes.c_ulong), # milliseconds
              ('idle',        ctypes.c_ulong), # milliseconds
              ('event_mask',  ctypes.c_ulong)] # events

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

