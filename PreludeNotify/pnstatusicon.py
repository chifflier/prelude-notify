# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Sebastien Tricaud <toady@inl.fr>
#         Alexandre De Dommelin <adedommelin@tuxz.net> 
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

import gtk
import gobject

import pnconfig


class PreludeStatusIcon:

        def __init__(self, gloop, config):
                self.config = config
                self.gloop = gloop
                self.icon = gtk.status_icon_new_from_file(self.config.getIconOk())
                self.icon.connect('popup-menu', self.menu)

        def MissedAlerts(self):
                self.icon.set_from_file(self.config.getIconBad())

        def SeenAlerts(self):
                self.icon.set_from_file(self.config.getIconOk())

        def menu(self, icon, event_button, event_time):
                m = gtk.Menu()

                item = gtk.ImageMenuItem(gtk.STOCK_EXECUTE, 'Configure...')
                label = item.get_children()[0]
                label.set_label("Configure...")
                item.connect('activate', self.configure)
                item.show()
                m.append(item)
                item = gtk.SeparatorMenuItem()
                item.show()
                m.append(item)
                item = gtk.ImageMenuItem(gtk.STOCK_ABOUT, 'About')
                item.connect('activate', self.about)
                item.show()
                m.append(item)
                item = gtk.ImageMenuItem(gtk.STOCK_QUIT, 'Quit')
                item.connect('activate', self.quit)
                item.show()
                m.append(item)

                m.popup(None, None, gtk.status_icon_position_menu, event_button,
                        event_time, icon)

        def configure(self, widget):
                dialog = gtk.Dialog("Configure prelude notify", None, 0,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

                profile_entry      = gtk.Entry()
                prewikka_url_entry = gtk.Entry()
                idle_entry         = gtk.Entry()
                threshold_entry    = gtk.Entry()
                idmef_filter_entry = gtk.Entry()
                manager_addr_entry = gtk.Entry()
                theme_entry        = gtk.Entry()

                table = gtk.Table(2,7)
                table.set_row_spacings(4)
                table.set_col_spacings(4)

                dialog.vbox.pack_start(table, False, False, 0)

                label = gtk.Label("Profile: ")
                table.attach(label, 0, 1, 0, 1)
                profile_entry.set_text(self.config.get("idmef","profile"))
                table.attach(profile_entry, 1, 2, 0, 1)
                label = gtk.Label("Manager Addresses: ")
                table.attach(label, 0, 1, 1, 2)
                manager_addr_entry.set_text(self.config.get("manager", "addresses"))
                table.attach(manager_addr_entry, 1, 2, 1, 2)
                label = gtk.Label("IDMEF filter: ")
                table.attach(label, 0, 1, 2, 3)
                idmef_filter_entry.set_text(self.config.get("idmef", "filter"))
                table.attach(idmef_filter_entry, 1, 2, 2, 3)
                idlecheck = gtk.CheckButton("Idle: ")
                idlecheck.connect('toggled', self.idle_toggled, idle_entry)
                idletime = self.config.get("general", "x11_idle_timeout")
                if idletime:
                        idlecheck.set_active(True)
                        idle_entry.set_editable(True)
                else:
                        idlecheck.set_active(False)
                        idle_entry.set_editable(False)
                table.attach(idlecheck, 0, 1, 3, 4)
                table.attach(idle_entry, 1, 2, 3, 4)
                idle_entry.set_text(self.config.get("general", "x11_idle_timeout"))
                threshold = gtk.Label("Threshold: ")
                table.attach(threshold, 0, 1, 4, 5)
                table.attach(threshold_entry, 1, 2, 4, 5)
                threshold_entry.set_text(self.config.get("general", "threshold_timeout"))
                label = gtk.Label("Prewikka URL: ")
                table.attach(label, 0, 1, 5, 6)
                prewikka_url_entry.set_text(self.config.get("prewikka", "url"))
                table.attach(prewikka_url_entry, 1, 2, 5, 6)
                label = gtk.Label("Theme: ")
                table.attach(label, 0, 1, 6, 7)
                theme_entry.set_text(self.config.get("ui", "theme"))
                table.attach(theme_entry, 1, 2, 6, 7)

                dialog.show_all()
                response = dialog.run()

                if response == gtk.RESPONSE_OK:
                        self.config.set("idmef", "profile", profile_entry.get_text())
                        self.config.set("manager", "addresses", manager_addr_entry.get_text())
                        self.config.set("idmef", "filter", idmef_filter_entry.get_text())
                        self.config.set("prewikka", "url", prewikka_url_entry.get_text())
                        self.config.set("ui", "theme", theme_entry.get_text())
                        self.config.set("general", "threshold_timeout", threshold_entry.get_text())
                        if idlecheck.get_active():
                                self.config.set("general", "x11_idle_timeout", idle_entry.get_text())
                        else:
                                self.config.set("general", "x11_idle_timeout", "")

                        self.config.update()

                dialog.destroy()

        def about(self, widget):
                dialog = gtk.AboutDialog()
                try:
                        dialog.set_program_name("Prelude Notify")
                except AttributeError:
                        print "Cannot add the dialog program name"
                try:
                        dialog.set_copyright("Sebastien Tricaud, Alexandre De Dommelin (c) 2010")
                except AttributeError:
                        print "Cannot add the dialog copyright"
                try:
                        dialog.set_comments("Systray Notification for Prelude IDS")
                except AttributeError:
                        print "Cannot add the dialog comments"
                dialog.run()
                dialog.destroy()

        def quit(self, widget):
                self.gloop.quit()

        #
        # Callbacks
        #
        def idle_toggled(self, widget, idle_entry):
                if widget.get_active():
                        idle_entry.set_editable(True)
                else:
                        idle_entry.set_editable(False)
