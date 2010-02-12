#!/usr/bin/env python

import os, glob
from distutils.core import setup
from distutils.command.install import install

_VERSION="0.9.1"

class my_install(install):
   def init_siteconfig(self):
        config = open("PreludeNotify/siteconfig.py", "w")
        print >> config, "prefix = '%s'" % os.path.abspath(self.prefix)
        print >> config, "conf_dir = '/etc/prelude-notify'"
        print >> config, "version = '%s'" % _VERSION
        config.close()

   def run(self):
        os.umask(022)
        self.init_siteconfig()
        install.run(self)



setup(name="prelude-notify",
      version=_VERSION,
      maintainer = "Alexandre De Dommelin",
      maintainer_email = "adedommelin@tuxz.net",
      url = "http://www.prelude-ids.com",
      packages=[ 'PreludeNotify' ],
      data_files=[ ("share/prelude-notify/themes/default", glob.glob("pixmaps/themes/default/*")),
                   ("share/prelude-notify/themes/default/tray", glob.glob("pixmaps/themes/tray/*")),
                   ("share/applications", ["prelude-notify.desktop"]),
                   ("/etc/prelude-notify", ["prelude-notify.conf"]) ],
      scripts=[ "prelude-notify" ],
      cmdclass={ 'install': my_install } )
