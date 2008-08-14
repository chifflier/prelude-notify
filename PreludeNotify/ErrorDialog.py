# Copyright (C) 2008 PreludeIDS Technologies. All Rights Reserved.
# Author: Sebastien Tricaud <toady@inl.fr>
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
