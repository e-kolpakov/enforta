__author__ = 'john'
import os
import sys

from base import *

local_settings_file = os.environ.get('EnvironmentType', 'development')

if 'migrate' in sys.argv or 'syncdb' in sys.argv:
    local_settings_file = 'database_migration'

# sys.stderr.write("Importing local settings from {0}\n".format(local_settings_file))

try:
    _imported = __import__(local_settings_file, globals(), locals(), [], -1)
    for setting in dir(_imported):
        if setting == setting.upper():
            locals()[setting] = getattr(_imported, setting)
except ImportError:
    pass

# a little fix to allow a slightly larger than limit files to still hit the form validations
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE + 15 * 2 ** 20