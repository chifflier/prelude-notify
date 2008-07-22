import gtk
import pnconfig

class PreludeStatusIcon():
	profile_entry      = gtk.Entry()
	prewikka_url_entry = gtk.Entry()
	idmef_filter_entry = gtk.Entry()
	manager_addr_entry = gtk.Entry()
	theme_entry        = gtk.Entry()

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
		dialog = gtk.Dialog("Configure prelude notify", None, 0,
			(gtk.STOCK_OK, gtk.RESPONSE_OK,
			 gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

		table = gtk.Table(2,6)
		table.set_row_spacings(4)
        	table.set_col_spacings(4)

		dialog.vbox.pack_start(table, False, False, 0)

		label = gtk.Label("Profile: ")
		table.attach(label, 0, 1, 0, 1)
		table.attach(self.profile_entry, 1, 2, 0, 1)
		label = gtk.Label("Manager Address: ")
		table.attach(label, 0, 1, 1, 2)
		table.attach(self.manager_addr_entry, 1, 2, 1, 2)
		label = gtk.Label("IDMEF filter: ")
		table.attach(label, 0, 1, 2, 3)
		table.attach(self.idmef_filter_entry, 1, 2, 2, 3)
		label = gtk.Label("Prewikka URL: ")
		table.attach(label, 0, 1, 3, 4)
		table.attach(self.prewikka_url_entry, 1, 2, 3, 4)
		label = gtk.Label("Theme: ")
		table.attach(label, 0, 1, 4, 5)
		table.attach(self.theme_entry, 1, 2, 4, 5)

		dialog.show_all()
		response = dialog.run()

		if response == gtk.RESPONSE_OK:
			print "OK"
            		#self.entry1.set_text(local_entry1.get_text())
            		#self.entry2.set_text(local_entry2.get_text())

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

