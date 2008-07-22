import gtk
import pnconfig

class PreludeStatusIcon():
	def __init__(self):
		icon = gtk.status_icon_new_from_file(pnconfig.iconok)


