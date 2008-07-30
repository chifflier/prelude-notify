import os
import gtk

class CreateProfile:
	def __init__(self, client, perms, profilename):
		dlgstring = "Please register your Prelude agent. Run as root:\nprelude-admin register \"%s\" \"idmef:r\" 127.0.0.1 --uid %d --gid %d" % (profilename, os.getuid(), os.getgid())
                dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, dlgstring)

                dialog.show_all()
                response = dialog.run()

                dialog.destroy()

