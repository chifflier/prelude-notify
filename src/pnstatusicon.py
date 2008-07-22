import gtk
import pnconfig

class PreludeStatusIcon():
	def __init__(self):
		icon = gtk.status_icon_new_from_file(pnconfig.iconok)
		icon.connect('popup-menu', self.menu)

	def menu(self, icon, event_button, event_time):
		m = gtk.Menu()

		item = gtk.MenuItem('Configure...')
		item.connect('activate', self.configure)
		item.show()
		m.append(item)
		item = gtk.MenuItem('About')
		item.connect('activate', self.about)
		item.show()
		m.append(item)
		item = gtk.MenuItem('Quit')
		item.connect('activate', self.quit)
		item.show()
		m.append(item)

		m.popup(None, None, gtk.status_icon_position_menu, event_button,
			event_time, icon)

	def configure(self, data):
		print "Run the configure window"

	def about(self, data):
		print "Run the about window"

	def quit(self, data):
		gtk.main_quit()

