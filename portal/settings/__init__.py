__author__ = 'john'
from base import *

import os
import sys

local_settings_file = os.environ.get('EnvironmentType', 'development')

if 'migrate' in sys.argv or 'syncdb' in sys.argv:
    local_settings_file = 'database_migration'

sys.stderr.write("Importing local settings from %s\n" % local_settings_file)

try:
    _imported = __import__(local_settings_file, globals(), locals(), [], -1)
    for setting in dir(_imported):
        if setting == setting.upper():
            locals()[setting] = getattr(_imported, setting)
except ImportError:
    pass