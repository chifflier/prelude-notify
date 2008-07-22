import gtk
import pnconfig

class PreludeStatusIcon():
	profile_entry      = gtk.Entry()
	prewikka_url_entry = gtk.Entry()
	idmef_filter_entry = gtk.Entry()
	manager_addr_entry = gtk.Entry()
	theme_entry        = gtk.Entry()

	def __init__(self, config):
		icon = gtk.status_icon_new_from_file(pnconfig.iconok)
		icon.connect('popup-menu', self.menu)
		self.config = config

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
		dialog = gtk.Dialog("Configure prelude notify", None, 0,
			(gtk.STOCK_OK, gtk.RESPONSE_OK,
			 gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

		table = gtk.Table(2,6)
		table.set_row_spacings(4)
        	table.set_col_spacings(4)

		dialog.vbox.pack_start(table, False, False, 0)

		label = gtk.Label("Profile: ")
		table.attach(label, 0, 1, 0, 1)
		self.profile_entry.set_text(self.config.get("idmef", "profile"))
		table.attach(self.profile_entry, 1, 2, 0, 1)
		label = gtk.Label("Manager Addresses: ")
		table.attach(label, 0, 1, 1, 2)
		self.manager_addr_entry.set_text(self.config.get("manager", "addresses"))
		table.attach(self.manager_addr_entry, 1, 2, 1, 2)
		label = gtk.Label("IDMEF filter: ")
		table.attach(label, 0, 1, 2, 3)
		self.idmef_filter_entry.set_text(self.config.get("idmef", "filter"))
		table.attach(self.idmef_filter_entry, 1, 2, 2, 3)
		label = gtk.Label("Prewikka URL: ")
		table.attach(label, 0, 1, 3, 4)
		self.prewikka_url_entry.set_text(self.config.get("prewikka", "url"))
		table.attach(self.prewikka_url_entry, 1, 2, 3, 4)
		label = gtk.Label("Theme: ")
		table.attach(label, 0, 1, 4, 5)
		self.theme_entry.set_text(self.config.get("ui", "theme"))
		table.attach(self.theme_entry, 1, 2, 4, 5)

		dialog.show_all()
		response = dialog.run()

		if response == gtk.RESPONSE_OK:
			self.config.set("idmef", "profile", self.profile_entry.get_text())
			self.config.set("manager", "addresses", self.manager_addr_entry.get_text())
			self.config.set("idmef", "filter", self.idmef_filter_entry.get_text())
			self.config.set("prewikka", "url", self.prewikka_url_entry.get_text())
			self.config.set("ui", "theme", self.theme_entry.get_text())

        	dialog.destroy()


	def about(self, data):
		dialog = gtk.AboutDialog()
		dialog.set_program_name("Prelude Notify")
		dialog.set_copyright("Sebastien Tricaud (c) 2008")
		dialog.set_comments("Systray Notification for Prelude IDS")
		dialog.run()
		dialog.destroy()

	def quit(self, data):
		gtk.main_quit()

