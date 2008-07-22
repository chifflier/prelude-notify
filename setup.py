#!/usr/bin/env python

import os, glob
from distutils.core import setup
from distutils.command.install import install

_VERSION="0.0.0"

class my_install(install):
   def init_siteconfig(self):
        config = open("PreludeNotify/siteconfig.py", "w")
        print >> config, "prefix = '%s'" % os.path.abspath(self.prefix)
        print >> config, "version = '%s'" % _VERSION
        config.close()

   def run(self):
        os.umask(022)
        self.init_siteconfig()
        install.run(self)



setup(name="prelude-notify",
      version=_VERSION,
      maintainer = "Sebastien Tricaud",
      maintainer_email = "toady@inl.fr",
      url = "http://www.prelude-ids.com",
      packages=[ 'PreludeNotify' ],
      data_files=[ ("share/prelude-notify/themes/default", glob.glob("pixmaps/themes/default/*")) ],
      scripts=[ "prelude-notify" ],
      cmdclass={ 'install': my_install } )
