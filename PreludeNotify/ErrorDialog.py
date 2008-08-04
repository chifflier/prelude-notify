import os
import gtk

class ErrorDialog:
        def __init__(self, content):
                dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, content)

                dialog.show_all()
                response = dialog.run()

                dialog.destroy()

class CreateProfile(ErrorDialog):
        def __init__(self, profilename, manager_addr):
                dlgstring = "Please register your Prelude agent. Run as root:\nprelude-admin register \"%s\" \"idmef:r\" %s --uid %d --gid %d" % (profilename, manager_addr, os.getuid(), os.getgid())
                ErrorDialog.__init__(self, dlgstring)
