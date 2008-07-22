#!/usr/bin/env python

import sys
import os, os.path
import stat
import glob

from distutils.core import setup

_VERSION="0.0.0"

setup(name="prelude-notify",
      version=_VERSION,
      maintainer = "Sebastien Tricaud",
      maintainer_email = "toady@inl.fr",
      url = "http://www.prelude-ids.com",
      packages=[ 'PreludeNotify' ],
      data_files=[ ("share/prelude-notify/themes/default", glob.glob("pixmaps/themes/default/*")) ],
      scripts=[ "prelude-notify" ])
